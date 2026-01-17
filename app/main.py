from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Students API")

class StudentCreate(BaseModel):
    name: str

class Student(StudentCreate):
    id: int

class GroupCreate(BaseModel):
    name: str

class Group(GroupCreate):
    id: int
    students: List[int] = []

students: Dict[int, Student] = {}
groups: Dict[int, Group] = {}

student_id_counter = 1
group_id_counter = 1

@app.post("/students", response_model=Student)
def create_student(student: StudentCreate):
    global student_id_counter
    new_student = Student(id=student_id_counter, name=student.name)
    students[student_id_counter] = new_student
    student_id_counter += 1
    return new_student

@app.get("/students", response_model=List[Student])
def get_students():
    return list(students.values())

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted"}

@app.post("/groups", response_model=Group)
def create_group(group: GroupCreate):
    global group_id_counter
    new_group = Group(id=group_id_counter, name=group.name, students=[])
    groups[group_id_counter] = new_group
    group_id_counter += 1
    return new_group

@app.get("/groups", response_model=List[Group])
def get_groups():
    return list(groups.values())

@app.get("/groups/{group_id}", response_model=Group)
def get_group(group_id: int):
    if group_id not in groups:
        raise HTTPException(status_code=404, detail="Group not found")
    return groups[group_id]

@app.delete("/groups/{group_id}")
def delete_group(group_id: int):
    if group_id not in groups:
        raise HTTPException(status_code=404, detail="Group not found")
    del groups[group_id]
    return {"message": "Group deleted"}

@app.post("/groups/{group_id}/students/{student_id}")
def add_student_to_group(group_id: int, student_id: int):
    if group_id not in groups or student_id not in students:
        raise HTTPException(status_code=404, detail="Group or student not found")
    if student_id not in groups[group_id].students:
        groups[group_id].students.append(student_id)
    return {"message": "Student added to group"}

@app.delete("/groups/{group_id}/students/{student_id}")
def remove_student_from_group(group_id: int, student_id: int):
    if group_id not in groups:
        raise HTTPException(status_code=404, detail="Group not found")
    if student_id in groups[group_id].students:
        groups[group_id].students.remove(student_id)
    return {"message": "Student removed from group"}

@app.get("/groups/{group_id}/students", response_model=List[Student])
def get_students_in_group(group_id: int):
    if group_id not in groups:
        raise HTTPException(status_code=404, detail="Group not found")
    return [students[s_id] for s_id in groups[group_id].students]

@app.post("/groups/transfer")
def transfer_student(student_id: int, from_group_id: int, to_group_id: int):
    if from_group_id not in groups or to_group_id not in groups:
        raise HTTPException(status_code=404, detail="Group not found")
    if student_id not in groups[from_group_id].students:
        raise HTTPException(status_code=400, detail="Student not in source group")
    groups[from_group_id].students.remove(student_id)
    groups[to_group_id].students.append(student_id)
    return {"message": "Student transferred"}
