"""
Students Database CRUD Application
FastAPI + SQLite | EWB Internship Project
"""
import sqlite3
from contextlib import contextmanager
from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field, model_validator

app = FastAPI(
    title="Students CRUD API",
    description="Create, Read, Update, Delete student records (FastAPI + SQLite)",
)

DB_NAME = "students.db"


# ---------- Database setup ----------
@contextmanager
def db():
    """Connection kholta hai, kaam ke baad commit aur close kar deta hai."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # rows ko dict jaisa use kar sakein
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dob TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                course TEXT,
                address TEXT,
                enrollment_date TEXT
            )
        """)


init_db()


# ---------- Validation models ----------
class StudentCreate(BaseModel):
    name: str = Field(min_length=2)
    dob: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    @model_validator(mode="after")
    def check_rules(self):
        if not self.email and not self.phone:
            raise ValueError("Email ya phone mein se kam se kam ek dena zaroori hai")
        if self.dob >= date.today():
            raise ValueError("Date of birth aaj se pehle ki honi chahiye")
        return self


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    dob: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None


# ---------- CREATE ----------
@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    data = student.model_dump(mode="json")
    try:
        with db() as conn:
            cur = conn.execute(
                """INSERT INTO students
                   (name, dob, email, phone, course, address, enrollment_date)
                   VALUES (:name, :dob, :email, :phone, :course, :address, :enrollment_date)""",
                data,
            )
            return {"id": cur.lastrowid, **data}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ye email already exist karta hai")


# ---------- READ ALL (+ filter) ----------
@app.get("/students")
def list_students(
    name: Optional[str] = None,
    course: Optional[str] = None,
    born_after: Optional[int] = Query(None, description="Is saal ke baad paida hue, e.g. 2005"),
):
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if course:
        query += " AND course LIKE ?"
        params.append(f"%{course}%")
    if born_after:
        query += " AND CAST(substr(dob, 1, 4) AS INTEGER) > ?"
        params.append(born_after)
    query += " ORDER BY id"
    with db() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


# ---------- READ ONE ----------
@app.get("/students/{student_id}")
def get_student(student_id: int):
    with db() as conn:
        row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return dict(row)


# ---------- UPDATE ----------
@app.patch("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    changes = student.model_dump(mode="json", exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Update ke liye koi field do")
    try:
        with db() as conn:
            exists = conn.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
            if exists is None:
                raise HTTPException(status_code=404, detail="Student not found")
            set_clause = ", ".join(f"{field} = ?" for field in changes)
            conn.execute(
                f"UPDATE students SET {set_clause} WHERE id = ?",
                (*changes.values(), student_id),
            )
            row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            return dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ye email already use mein hai")


# ---------- DELETE ----------
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with db() as conn:
        cur = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
