from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from database import engine,SessionLocal,Base
from model import Task
from pydantic import BaseModel
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TaskCreate(BaseModel):
    title : str
    description: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.post("/tasks") 
async def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}")
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


