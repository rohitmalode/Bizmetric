# ERD, UML & Bill Generation

This folder contains files demonstrating Python integration with SQL Server (SSMS) along with bill generation functionality. The main purpose is to accept user input for hotel transactions, store data in the database, and optionally generate a bill in `.txt` format.  

## Contents
- **Python Script (`.py`)** – Connects Python (VS Code) to SQL Server and allows:
  - Storing customer orders and transaction data in the database.
  - Updating tables dynamically based on user input.
  - Generating a hotel bill as a `.txt` file if the customer requests.
- **Images (`.png`, `.jpg`)** – ERD (Entity Relationship Diagram) and UML diagram for database structure and workflow.

## Usage
1. Open the Python script in VS Code.
2. Ensure SQL Server (SSMS) is running and the database credentials in the script are correct.
3. Run the script in Python 3.x environment.
4. Input customer and order details as prompted.
5. If the customer wants a bill, the script will generate a `.txt` file with the transaction summary.
6. Verify stored data directly in SSMS tables if needed.

## Notes
- This folder demonstrates practical usage of Python for database operations and bill generation.
- Make sure Python 3.x and required libraries (e.g., `pyodbc` or `pymssql`) are installed.
