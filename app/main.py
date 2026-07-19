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


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task.filter(Task.id == task_id).first())
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task


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