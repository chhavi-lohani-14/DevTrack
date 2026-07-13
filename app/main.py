from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    priority: str

tasks = []


@app.get("/")
def home():
    return {"message": "Welcome to DevTrack!"}


@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return task


@app.get("/tasks")
def get_tasks():
    return tasks