# Bill Printing

This folder contains files demonstrating Python integration with a SQL Server database (SSMS) and related diagrams. The main purpose is to connect Python scripts to a database, accept user input, and store or update data in the database tables.  

## Contents
- **Python Script (`.py`)** – Connects Python (VS Code) to SQL Server (SSMS) and allows data insertion based on user input.
- **Images (`.png`, `.jpg`)** – ERD (Entity Relationship Diagram) and UML diagram for the database and application structure.
- Demonstrates:
  - Establishing a connection between Python and SQL Server.
  - Accepting user input in Python terminal.
  - Storing input data in SQL Server tables.
  - Reflecting changes in the database dynamically.

## Usage
1. Open the Python script in VS Code.
2. Ensure SQL Server (SSMS) is running and the database credentials in the script are correct.
3. Run the script in Python 3.x environment.
4. Input values as prompted in the terminal; the script will store or update data in the SQL Server database.
5. You can verify changes directly in SSMS by querying the relevant tables.

## Notes
- This folder is intended for learning and practice with Python-to-database connectivity.
- Make sure Python 3.x and required libraries (e.g., `pyodbc` or `pymssql`) are installed before running the script.

