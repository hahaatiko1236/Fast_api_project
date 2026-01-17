from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str

class StudentOut(BaseModel):
    id: int
    name: str
    group_id: int | None

    class Config:
        orm_mode = True
