# Restaurant Order Management System
# ----------------------------------
# Create a system using classes and functions to handle restaurant orders:
#
# 1. Take Order: Store customer orders in a dictionary.
# 2. Deliver Order: Mark the ordered items as delivered.
# 3. Generate Bill: Calculate the total cost of the delivered items.
# 4. Print Bill: Display the bill details.
# 5. Hard Copy Option: Ask the user if they want a hard copy of the bill or just print it.



import os
from datetime import datetime


class Hotel:
    def __init__(self, hotel_name):
        self.hotel_name = hotel_name
        self.customer_name = ""
        self.orders = {}
        self.total = 0

    # Take Order
    def take_order(self):
        self.customer_name = input("Enter Customer Name: ")

        while True:
            menu = input("Enter Menu Item: ")
            quantity = int(input("Enter Quantity: "))
            price = float(input("Enter Price per Item: "))

            # If item already exists, update quantity
            if menu in self.orders:
                self.orders[menu]["quantity"] += quantity
                self.orders[menu]["total"] += quantity * price
            else:
                self.orders[menu] = {
                    "quantity": quantity,
                    "price": price,
                    "total": quantity * price
                }

            more = input("Add more items? (yes/no): ").lower()
            if more != "yes":
                break

    # Deliver Order
    def deliver_order(self):
        print("\n✅ Order Delivered Successfully!")

    # Generate Bill
    def generate_bill(self):
        self.total = sum(item["total"] for item in self.orders.values())

    # Print or Save Bill
    def print_bill(self):
        print_option = input("Do you want Hard Copy? (yes/no): ").lower()

        bill_content = "\n" + "-" * 60 + "\n"
        bill_content += f"{self.hotel_name.center(60)}\n"
        bill_content += "-" * 60 + "\n"
        bill_content += f"Customer Name: {self.customer_name}\n"
        bill_content += "-" * 60 + "\n"
        bill_content += "{:<5} {:<15} {:<10} {:<10} {:<10}\n".format(
            "SR", "Item", "Qty", "Price", "Total"
        )
        bill_content += "-" * 60 + "\n"

        for idx, (item, details) in enumerate(self.orders.items(), start=1):
            bill_content += "{:<5} {:<15} {:<10} {:<10} {:<10}\n".format(
                idx,
                item,
                details["quantity"],
                details["price"],
                details["total"],
            )

        bill_content += "-" * 60 + "\n"
        bill_content += "{:<40} {:>15}\n".format("Grand Total:", self.total)
        bill_content += "-" * 60 + "\n"

        if print_option == "yes":
            folder_path = r"D:\BILL\CLASS HOTEL BILL"

            # Create folder if not exists
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Clean customer name for filename (remove spaces)
            clean_name = self.customer_name.replace(" ", "_")

            # Create file name using customer name + datetime
            file_name = clean_name + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
            full_path = os.path.join(folder_path, file_name)

            with open(full_path, "w") as file:
                file.write(bill_content)

            print(f"\n📄 Bill saved successfully at:\n{full_path}")

        else:
            print(bill_content)


# ---------------- Main Program ----------------

hotel_name = input("Enter Hotel Name: ")
hotel = Hotel(hotel_name)

hotel.take_order()
hotel.deliver_order()
hotel.generate_bill()
hotel.print_bill()
