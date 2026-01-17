from fastapi import FastAPI
from app.api import students, groups
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students API")

app.include_router(students.router)
app.include_router(groups.router)
