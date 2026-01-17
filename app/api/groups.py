from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.group import GroupCreate, GroupOut
from app.services.group_service import create_group, add_student_to_group
from app.models.group import Group

router = APIRouter(prefix="/groups", tags=["Groups"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=GroupOut)
def create(group: GroupCreate, db: Session = Depends(get_db)):
    return create_group(db, group.name)

@router.post("/{group_id}/students/{student_id}")
def add_student(group_id: int, student_id: int, db: Session = Depends(get_db)):
    student, group = add_student_to_group(db, student_id, group_id)
    if not student or not group:
        raise HTTPException(404, "Student or Group not found")
    return {"status": "student added"}
