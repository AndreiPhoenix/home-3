import pandas as pd
from sqlalchemy.orm import Session
from models import Student

class StudentDatabase:
    def __init__(self, session_factory):
        self.Session = session_factory

    def insert_students(self, students):
        session = self.Session()
        session.add_all(students)
        session.commit()
        session.close()

    def load_data_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        students = [
            Student(last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    faculty=row['Факультет'],
                    course=row['Курс'],
                    grade=row['Оценка'])
            for _, row in df.iterrows()
        ]
        self.insert_students(students)

    def get_students_by_faculty(self, faculty_name):
        session = self.Session()
        students = session.query(Student).filter(Student.faculty == faculty_name).all()
        session.close()
        return students

    def get_unique_courses(self):
        session = self.Session()
        courses = session.query(Student.course).distinct().all()
        session.close()
        return [course[0] for course in courses]

    def get_average_grade_by_faculty(self, faculty_name):
        session = self.Session()
        average_grade = session.query(func.avg(Student.grade)).filter(Student.faculty == faculty_name).scalar()
        session.close()
        return average_grade
