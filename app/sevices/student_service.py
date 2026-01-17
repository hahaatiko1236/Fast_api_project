from sqlalchemy.orm import Session
from app.models.student import Student

def create_student(db: Session, name: str):
    student = Student(name=name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = db.get(Student, student_id)
    if student:
        db.delete(student)
        db.commit()
    return student
