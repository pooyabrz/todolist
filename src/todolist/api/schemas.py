from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: int = Field(2, ge=1, le=3, description="1=Low, 2=Medium, 3=High")
    category_name: Optional[str] = Field(None, max_length=100)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=3)
    category_name: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True

class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int
    overdue: int