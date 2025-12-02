from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStats
from ...services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = None,
    q: Optional[str] = None,
    service: TaskService = Depends(get_task_service),
):
    return service.get_tasks(skip=skip, limit=limit, completed=completed, search=q)

@router.get("/stats", response_model=TaskStats)
def get_statistics(service: TaskService = Depends(get_task_service)):
    return service.get_statistics()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        priority=task_in.priority,
        category_name=task_in.category_name,
    )

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate, service: TaskService = Depends(get_task_service)):
    task = service.update_task(
        task_id=task_id,
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        priority=task_in.priority,
        category_name=task_in.category_name,
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.complete_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")