# Restaurant Order Management System
# ----------------------------------
# Create a system using classes and functions to handle restaurant orders:
#
# 1. Take Order: Store customer orders in a dictionary.
# 2. Deliver Order: Mark the ordered items as delivered.
# 3. Generate Bill: Calculate the total cost of the delivered items.
# 4. Print Bill: Display the bill details.
# 5. Hard Copy Option: Ask the user if they want a hard copy of the bill or just print it.




import pyodbc
from datetime import datetime
import os

# ==============================
# DATABASE CONNECTION
# ==============================

conn = pyodbc.connect(
    r'Driver={ODBC Driver 17 for SQL Server};'
    r'Server=.\SQLEXPRESS;'
    r'Database=RESTAURANT_RMS;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()


# ==============================
# TABLE MANAGER
# ==============================

class TableManager:

    def show_tables(self):
        print("\n------ TABLE STATUS ------")
        cursor.execute("SELECT * FROM Tables")
        for row in cursor.fetchall():
            print(f"Table {row.table_id:<5} {row.status}")
        print("--------------------------")

    def is_available(self, table_id):
        cursor.execute("SELECT status FROM Tables WHERE table_id=?", table_id)
        row = cursor.fetchone()
        return row and row[0] == "Available"

    def occupy(self, table_id):
        cursor.execute("UPDATE Tables SET status='Occupied' WHERE table_id=?", table_id)
        conn.commit()

    def free(self, table_id):
        cursor.execute("UPDATE Tables SET status='Available' WHERE table_id=?", table_id)
        conn.commit()


# ==============================
# ORDER MANAGER
# ==============================

class OrderManager:

    def show_menu(self):
        print("\n" + "=" * 50)
        print("MENU".center(50))
        print("=" * 50)
        print(f"{'ID':<5}{'Item':<20}{'Price':>10}")
        print("-" * 50)

        cursor.execute("SELECT * FROM Menu")
        for row in cursor.fetchall():
            print(f"{row.item_id:<5}{row.name:<20}₹{row.price:>8}")

        print("=" * 50)

    def create_order(self, table_id):
        cursor.execute(
            "INSERT INTO Orders (table_id, status) VALUES (?, 'Preparing')",
            table_id
        )
        conn.commit()

        cursor.execute("SELECT @@IDENTITY")
        return cursor.fetchone()[0]

    def add_items(self, order_id):

        while True:
            item_name = input("Enter item name: ").strip()
            qty = int(input("Enter quantity: "))

            cursor.execute(
                "SELECT item_id, price FROM Menu WHERE LOWER(name)=LOWER(?)",
                item_name
            )
            row = cursor.fetchone()

            if not row:
                print("Item not found.")
                continue

            item_id, price = row
            total = float(price) * qty

            cursor.execute("""
                INSERT INTO Order_Details
                (order_id, item_id, quantity, price, total)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, item_id, qty, price, total))

            conn.commit()

            more = input("Add more items? (yes/no): ").lower()
            if more != "yes":
                break


# ==============================
# BILLING & PAYMENT MANAGER
# ==============================

class BillingManager:

    def generate_table_bill(self, table_id):

        cursor.execute("""
            SELECT o.order_id, m.name, od.quantity, od.price, od.total
            FROM Orders o
            JOIN Order_Details od ON o.order_id = od.order_id
            JOIN Menu m ON m.item_id = od.item_id
            WHERE o.table_id=? AND o.status!='Closed'
        """, table_id)

        rows = cursor.fetchall()

        if not rows:
            print("No open orders for this table.")
            return None, 0

        width = 70
        bill_text = ""
        bill_text += f"\n{'RESTAURANT BILL'.center(width)}\n"
        bill_text += "=" * width + "\n"
        bill_text += f"Table No : {table_id}\n"
        bill_text += f"Date     : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        bill_text += "=" * width + "\n"
        bill_text += f"{'Item':<20}{'Qty':<10}{'Price':<15}{'Total':<15}\n"
        bill_text += "-" * width + "\n"

        grand_total = 0

        for order_id, name, qty, price, total in rows:
            bill_text += f"{name:<20}{qty:<10}₹{price:<14.2f}₹{total:<14.2f}\n"
            grand_total += total

        bill_text += "-" * width + "\n"
        bill_text += f"{'Grand Total':<45}₹{grand_total:.2f}\n"
        bill_text += "=" * width + "\n"

        return bill_text, grand_total

    def process_payment(self, table_id, amount):

        mode = input("Payment Mode (Cash/Card/UPI): ")

        # Get all open order IDs for that table
        cursor.execute("""
            SELECT order_id
            FROM Orders
            WHERE table_id=? AND status!='Closed'
        """, table_id)

        orders = cursor.fetchall()

        if not orders:
            print("No pending orders.")
            return False

        # Insert payment per order (professional design)
        for order in orders:
            cursor.execute("""
                INSERT INTO Payments (order_id, amount, payment_mode)
                VALUES (?, ?, ?)
            """, (order.order_id, amount, mode))

        # Close all those orders
        cursor.execute("""
            UPDATE Orders
            SET status='Closed'
            WHERE table_id=? AND status!='Closed'
        """, table_id)

        conn.commit()
        print("Payment Successful!")
        return True


# ==============================
# MAIN DRIVER / program control
# ==============================

table_manager = TableManager()
order_manager = OrderManager()
billing_manager = BillingManager()

while True:

    print("""
1 Show Tables
2 Show Menu
3 Take Order
4 Generate Bill
5 Exit
""")

    choice = input("Enter choice: ")

    if choice == "1":
        table_manager.show_tables()

    elif choice == "2":
        order_manager.show_menu()

    elif choice == "3":

        table_id = int(input("Enter Table Number: "))

        if table_manager.is_available(table_id):
            table_manager.occupy(table_id)
            print("Table Occupied.")

        order_id = order_manager.create_order(table_id)
        print(f"Order Created. Order ID: {order_id}")

        order_manager.add_items(order_id)

    elif choice == "4":

        table_id = int(input("Enter Table Number for Billing: "))

        bill_text, total = billing_manager.generate_table_bill(table_id)

        if bill_text is None:
            continue

        print("\nProcessing Payment...\n")

        success = billing_manager.process_payment(table_id, total)

        if not success:
            continue

        # After successful payment → print or save
        hardcopy = input("Do you want Hard Copy Bill? (yes/no): ").lower()

        if hardcopy == "yes":

            folder_path = r"C:\Users\brohi\Downloads\PYTHON SERVER\Bill print project"

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            filename = f"Bill_Table_{table_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            full_path = os.path.join(folder_path, filename)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(bill_text)

            print("Bill saved at:")
            print(full_path)

        else:
            print(bill_text)

        table_manager.free(table_id)
        print("Table is now Available.")

    elif choice == "5":
        break

    else:
        print("Invalid choice.")

conn.close()
