from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    priority: str

class Task(TaskCreate):
    id: int
    