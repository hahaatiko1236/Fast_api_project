from fastapi import FastAPI

app = FastAPI(title="Students FastAPI API")

@app.get("/")
def root():
    return {"message": "Students API is running"}

@app.get("/students")
def get_students():
    return []

@app.post("/students")
def create_student(student: dict):
    return student

@app.get("/groups")
def get_groups():
    return []

@app.post("/groups")
def create_group(group: dict):
    return group