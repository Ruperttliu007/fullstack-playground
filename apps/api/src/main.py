from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .db import Base, engine, SessionLocal
from .models import Task
from .schemas import TaskCreate, TaskRead, TaskUpdate
app = FastAPI(title="Playground API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@app.get("/health")              # 健康检查
def health(): return {"status":"ok"}
@app.get("/tasks", response_model=List[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id.desc()).all()
@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(p: TaskCreate, db: Session = Depends(get_db)):
    obj = Task(title=p.title, note=p.note); db.add(obj); db.commit(); db.refresh(obj); return obj
@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, p: TaskUpdate, db: Session = Depends(get_db)):
    obj = db.get(Task, task_id)
    if not obj: raise HTTPException(404, "Task not found")
    for k,v in p.model_dump(exclude_unset=True).items(): setattr(obj, k, v)
    db.commit(); db.refresh(obj); return obj
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    obj = db.get(Task, task_id)
    if not obj: raise HTTPException(404, "Task not found")
    db.delete(obj); db.commit()
