import pyodbc
from datetime import datetime
import os


# ==============================
# DATABASE MANAGER
# ==============================

class DatabaseManager:

    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                r'Driver={ODBC Driver 17 for SQL Server};'
                r'Server=.\SQLEXPRESS;'
                r'Database=STUDENT_FEE_DB;'
                r'Trusted_Connection=yes;'
            )
            self.cursor = self.conn.cursor()
            print("Database Connected Successfully.\n")
        except Exception as e:
            print("Database Connection Failed:", e)

    def save_student_record(self, data):
        try:
            self.cursor.execute("""
                INSERT INTO StudentFees
                (student_name, subject, analytics, hostel,
                 food_months, transport, course_fee,
                 hostel_fee, food_fee, transport_fee, total_fee)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)

            self.conn.commit()
            print("Data Saved Successfully in SQL Server.\n")

        except Exception as e:
            print(" Error Saving Data:", e)

    def close(self):
        self.conn.close()
        print(" Database Connection Closed.")


# ==============================
# STUDENT CLASS
# ==============================

class Student:

    VALID_SUBJECTS = ["HR", "Finance", "Marketing", "DS"]

    def __init__(self, name, subject, analytics, hostel, food_months, transport):

        if subject not in Student.VALID_SUBJECTS:
            raise ValueError("Invalid Subject Selected")

        if analytics not in ["Y", "N"]:
            raise ValueError("Analytics must be Y or N")

        if hostel not in ["Y", "N"]:
            raise ValueError("Hostel must be Y or N")

        if food_months < 0:
            raise ValueError("Food months cannot be negative")

        if transport not in ["semester", "annual"]:
            raise ValueError("Transport must be semester or annual")

        self.name = name
        self.subject = subject
        self.analytics = analytics
        self.hostel = hostel
        self.food_months = food_months
        self.transport = transport


# ==============================
# FEE CALCULATOR
# ==============================

class FeeCalculator:

    BASE_FEE = 200000
    HOSTEL_FEE = 200000
    FOOD_PER_MONTH = 2000
    TRANSPORT_PER_SEM = 13000

    def calculate(self, student):

        course_fee = self.BASE_FEE

        if student.analytics == "Y" and student.subject in ["HR", "Marketing"]:
            course_fee += self.BASE_FEE * 0.10

        hostel_fee = self.HOSTEL_FEE if student.hostel == "Y" else 0
        food_fee = student.food_months * self.FOOD_PER_MONTH

        if student.transport == "semester":
            transport_fee = self.TRANSPORT_PER_SEM
        else:
            transport_fee = self.TRANSPORT_PER_SEM * 2

        total = course_fee + hostel_fee + food_fee + transport_fee

        return {
            "course_fee": int(course_fee),
            "hostel_fee": int(hostel_fee),
            "food_fee": int(food_fee),
            "transport_fee": int(transport_fee),
            "total_fee": int(total)
        }


# ==============================
# BILL GENERATOR
# ==============================

class BillGenerator:

    def generate_bill_text(self, student, fees):

        width = 60
        bill = ""
        bill += "\n" + "STUDENT FEE BILL".center(width) + "\n"
        bill += "=" * width + "\n"
        bill += f"Name        : {student.name}\n"
        bill += f"Subject     : {student.subject}\n"
        bill += f"Analytics   : {student.analytics}\n"
        bill += f"Hostel      : {student.hostel}\n"
        bill += f"Food Months : {student.food_months}\n"
        bill += f"Transport   : {student.transport}\n"
        bill += "=" * width + "\n"
        bill += f"{'Course Fee':<30}₹{fees['course_fee']}\n"
        bill += f"{'Hostel Fee':<30}₹{fees['hostel_fee']}\n"
        bill += f"{'Food Fee':<30}₹{fees['food_fee']}\n"
        bill += f"{'Transport Fee':<30}₹{fees['transport_fee']}\n"
        bill += "-" * width + "\n"
        bill += f"{'TOTAL':<30}₹{fees['total_fee']}\n"
        bill += "=" * width + "\n"
        bill += f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"

        return bill

    def save_to_file(self, bill_text, student_name):

        try:
            folder_path = r"C:\Users\brohi\Downloads\PYTHON SERVER\Student Fee Bills"

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            filename = f"{student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            full_path = os.path.join(folder_path, filename)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(bill_text)

            print("📄 Bill Saved At:")
            print(full_path)

        except Exception as e:
            print("Error Saving File:", e)


# ==============================
# MAIN SYSTEM CONTROLLER
# ==============================

def run_system():

    db = DatabaseManager()
    calculator = FeeCalculator()
    biller = BillGenerator()

    while True:

        print("""
==============================
   STUDENT FEE MANAGEMENT
==============================
1. Add New Student
2. Exit
""")

        choice = input("Enter Choice: ")

        if choice == "1":

            try:
                name = input("Enter Student Name: ")
                subject = input("Enter Subject (HR/Finance/Marketing/DS): ")
                analytics = input("Analytics (Y/N): ").upper()
                hostel = input("Hostel (Y/N): ").upper()
                food_months = int(input("Food (How many months?): "))
                transport = input("Transport (semester/annual): ").lower()

                student = Student(name, subject, analytics, hostel, food_months, transport)
                fees = calculator.calculate(student)

                bill_text = biller.generate_bill_text(student, fees)

                print_option = input("Do you want Hard Copy Bill? (yes/no): ").lower()

                if print_option == "yes":
                    biller.save_to_file(bill_text, student.name)
                else:
                    print(bill_text)

                db.save_student_record((
                    student.name,
                    student.subject,
                    student.analytics,
                    student.hostel,
                    student.food_months,
                    student.transport,
                    fees["course_fee"],
                    fees["hostel_fee"],
                    fees["food_fee"],
                    fees["transport_fee"],
                    fees["total_fee"]
                ))

            except ValueError as ve:
                print("⚠ Input Error:", ve)

            except Exception as e:
                print("⚠ Unexpected Error:", e)

        elif choice == "2":
            break

        else:
            print("Invalid Choice. Try Again.")

    db.close()


if __name__ == "__main__":
    run_system()
