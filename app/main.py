from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TaskCreate(BaseModel):
    title: str
    priority: str

class Task(TaskCreate):
    id: int

tasks = []
next_id = 1


@app.get("/")
def home():
    return {"message": "Welcome to DevTrack!"}


@app.post("/tasks")
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, 
                    **task.model_dump())
    
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks