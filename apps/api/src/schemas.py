from pydantic import BaseModel
from typing import Optional
class TaskCreate(BaseModel):
    title: str
    note: Optional[str] = None
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    note: Optional[str] = None
class TaskRead(BaseModel):
    id: int; title: str; done: bool; note: Optional[str] = None
    class Config: from_attributes = True
