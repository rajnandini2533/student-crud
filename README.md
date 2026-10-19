# Students Database CRUD Application

EWB Edu Tech Internship Project - Python Backend Development.

A backend API to manage student records using Create, Read, Update and Delete (CRUD)
operations. Built with **FastAPI** and **SQLite**.

## Features
- Create, list, filter, view, update and delete students
- Filter by name, course, or birth year (`born_after`)
- Input validation (email format, phone length, valid date of birth)
- Missing record handling (404) and duplicate email handling (400)
- Data is stored permanently in SQLite (`students.db`)

## Student Fields
| Field | Required | Notes |
|-------|----------|-------|
| id | auto | unique student ID |
| name | yes | min 2 characters |
| dob | yes | format `YYYY-MM-DD` |
| email | one of email/phone | must be valid and unique |
| phone | one of email/phone | 10-15 characters |
| course | no | |
| address | no | |
| enrollment_date | no | format `YYYY-MM-DD` |

## Prerequisites
- Python 3.10 or higher

## Installation
```bash
git clone https://github.com/rajnandini2533/student-crud.git
cd student-crud
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

## Run
```bash
uvicorn main:app --reload
```
Open **http://127.0.0.1:8000/docs** to test the API in Swagger UI.

Optional dummy data: `python seed_data.py`

## API Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /students | Create a student |
| GET | /students | List / filter students (`name`, `course`, `born_after`) |
| GET | /students/{student_id} | View a student |
| PATCH | /students/{student_id} | Update student details |
| DELETE | /students/{student_id} | Delete a student |

## API Testing
1. Run the server and open `/docs`.
2. Click an endpoint, press **Try it out**, fill the data and press **Execute**.

Sample create request:
```json
POST /students
{
  "name": "Amit Kumar",
  "dob": "2004-05-15",
  "email": "amit@example.com",
  "phone": "9876543210",
  "course": "BTech CSE"
}
```
Sample update request:
```json
PATCH /students/1
{ "course": "BCA" }
```
Filter examples:
- `GET /students?course=BTech`
- `GET /students?born_after=2004`

## Project Structure
```
student-crud/
├── main.py            # API and database code
├── seed_data.py       # dummy data
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes
Only dummy data is used. No real student information or secrets are committed.
