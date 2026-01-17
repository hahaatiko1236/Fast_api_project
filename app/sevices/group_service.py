from sqlalchemy.orm import Session
from app.models.group import Group
from app.models.student import Student

def create_group(db: Session, name: str):
    group = Group(name=name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = db.get(Student, student_id)
    group = db.get(Group, group_id)
    if student and group:
        student.group_id = group.id
        db.commit()
    return student, group
