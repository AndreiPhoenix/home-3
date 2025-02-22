from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import init_db
from crud import StudentDatabase
import os

app = FastAPI()

# Инициализация базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
SessionLocal = init_db(DATABASE_URL)
db = StudentDatabase(SessionLocal)

@app.post("/load-data/")
def load_data(file_path: str):
    db.load_data_from_csv(file_path)
    return {"message": "Data successfully loaded from CSV"}

@app.get("/students/{faculty_name}")
def get_students(faculty_name: str):
    return db.get_students_by_faculty(faculty_name)

@app.get("/courses/")
def get_courses():
    return db.get_unique_courses()

@app.get("/avg-grade/{faculty_name}")
def get_avg_grade(faculty_name: str):
    return {"average_grade": db.get_average_grade_by_faculty(faculty_name)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
