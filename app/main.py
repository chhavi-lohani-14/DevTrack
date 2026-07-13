from fastapi import FastAPI, HTTPException
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


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    
    raise HTTPException(
        status_code=404, 
        detail="Task not found"
        )

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            task[index] = Task(
                id=task_id,
                **updated_task.model_dump()
            )
            return tasks[index]
        
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(index)
            return {"message": "Task deleted successfully", "task": deleted_task}
    
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )