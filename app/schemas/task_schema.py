from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):

    title: str

    description: Optional[str] = None

    priority: str = "medium"

    due_date: Optional[datetime] = None

    assigned_to_id: int


class TaskUpdate(BaseModel):

    title: Optional[str] = None

    description: Optional[str] = None

    status: Optional[str] = None

    priority: Optional[str] = None

    due_date: Optional[datetime] = None


class TaskAssign(BaseModel):

    assigned_to_id: int


class TaskResponse(BaseModel):

    id: int

    title: str

    description: Optional[str]

    status: str

    priority: str

    assigned_to_id: int

    class Config:
        orm_mode = True