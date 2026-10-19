"""Dummy students daalne ke liye (sirf testing). Chalao: python seed_data.py"""
import sqlite3
import main  # table bana deta hai

students = [
    ("Amit Kumar", "2004-05-15", "amit@example.com", "9876543210", "BTech CSE"),
    ("Priya Sharma", "2005-08-21", "priya@example.com", "9876500001", "BCA"),
    ("Rahul Verma", "2003-12-02", "rahul@example.com", "9876500002", "BTech IT"),
]

conn = sqlite3.connect(main.DB_NAME)
for s in students:
    conn.execute(
        "INSERT OR IGNORE INTO students (name, dob, email, phone, course) VALUES (?, ?, ?, ?, ?)", s
    )
conn.commit()
conn.close()
print("Dummy students add ho gaye!")
