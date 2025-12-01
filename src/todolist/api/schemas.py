from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="عنوان وظیفه")
    description: Optional[str] = Field(None, max_length=1000, description="توضیحات")
    due_date: Optional[datetime] = Field(None, description="تاریخ سررسید (ISO format)")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int
    overdue: int