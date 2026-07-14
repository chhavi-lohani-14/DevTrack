from fastapi import FastAPI, HTTPException, Depends
from app.schemas import TaskCreate, TaskResponse
from app.database import engine, Base, get_db
from app.models import Task
from sqlalchemy.orm import Session


app = FastAPI()
Base.metadata.create_all(bind=engine)

tasks = []
next_id = 1


@app.get("/")
def home():
    return {"message": "Welcome to DevTrack!"}


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate,
                db: Session = Depends(get_db)
):
    db_task = Task(
        title=task.title,
        priority=task.priority
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


'''@app.get("/tasks")
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
    )'''