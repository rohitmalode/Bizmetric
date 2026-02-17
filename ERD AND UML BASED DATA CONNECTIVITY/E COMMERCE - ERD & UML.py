##########################################
########### DATABASE CONNECTION ###########

import pyodbc
conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=DESKTOP-HML5HDS\\SQLEXPRESS;'
    'Database=python;'
    'Trusted_Connection=yes;'
)



cursor = conn.cursor()

# Execute Query (Correct Syntax)
cursor.execute('SELECT * FROM dbo.Customer')

# Fetch and Print Data
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close Connection
conn.close()







try:
    # ---------------------------------
    # 1️⃣ CONNECT TO DATABASE
    # ---------------------------------
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=DESKTOP-HML5HDS\\SQLEXPRESS;'
        'Database=python;'
        'Trusted_Connection=yes;'
    )

    cursor = conn.cursor()
    print("Connected to Database Successfully!\n")

    # ---------------------------------
    # 2️⃣ INSERT PRODUCT
    # ---------------------------------
    print("---- Enter Product Details ----")
    pid = int(input("Product ID: "))
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    category = input("Category: ")

    cursor.execute("""
        INSERT INTO Product (product_id, name, price, stock, category, hotel_id)
        VALUES (?, ?, ?, ?, ?, 1)
    """, pid, name, price, stock, category)

    conn.commit()
    print("Product inserted successfully!\n")

    # ---------------------------------
    # 3️⃣ INSERT CUSTOMER
    # ---------------------------------
    print("---- Enter Customer Details ----")
    cid = int(input("Customer ID: "))
    cname = input("Customer Name: ")
    email = input("Email: ")

    cursor.execute("""
        INSERT INTO Customer (customer_id, name, email)
        VALUES (?, ?, ?)
    """, cid, cname, email)

    conn.commit()
    print("Customer inserted successfully!\n")

    # ---------------------------------
    # 4️⃣ CREATE ORDER
    # ---------------------------------
    cursor.execute("""
        INSERT INTO Orders (customer_id, total_amount, status)
        VALUES (?, ?, ?)
    """, cid, 0, 'Created')

    conn.commit()

    # Get generated order_id safely
    cursor.execute("SELECT SCOPE_IDENTITY()")
    order_id = cursor.fetchone()[0]

    # ---------------------------------
    # 5️⃣ ADD ORDER ITEM
    # ---------------------------------
    quantity = int(input("Enter Quantity: "))

    cursor.execute("SELECT price FROM Product WHERE product_id = ?", pid)
    product_price = cursor.fetchone()[0]

    total_price = product_price * quantity

    cursor.execute("""
        INSERT INTO OrderItem (order_id, product_id, quantity, price)
        VALUES (?, ?, ?, ?)
    """, order_id, pid, quantity, total_price)

    # Update order total
    cursor.execute("""
        UPDATE Orders
        SET total_amount = ?
        WHERE order_id = ?
    """, total_price, order_id)

    conn.commit()
    print("Order created successfully!\n")

    # ---------------------------------
    # 6️⃣ PAYMENT
    # ---------------------------------
    method = input("Payment Method (UPI/Card/Cash): ")

    cursor.execute("""
        INSERT INTO Payment (order_id, payment_method, payment_status)
        VALUES (?, ?, ?)
    """, order_id, method, 'Success')

    cursor.execute("""
        UPDATE Orders
        SET status = 'Paid'
        WHERE order_id = ?
    """, order_id)

    conn.commit()

    print("\nPayment Successful!")
    print("All data saved in SQL Server successfully!")

    conn.close()

except Exception as e:
    print("Error:", e)
