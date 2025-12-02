from fastapi import APIRouter, Depends, HTTPException, status, Query
<<<<<<< HEAD
from typing import List, Optional
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStats
from ...services.task_service import TaskService
=======
from sqlalchemy.orm import Session
from typing import List, Optional

from ..dependencies import get_db
from ..schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStats
from ...services.task_service import TaskService     
from ...repositories.task_repository import TaskRepository
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
<<<<<<< HEAD
    return TaskService(db)
=======
    return TaskService(TaskRepository(db))
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = None,
    q: Optional[str] = None,
<<<<<<< HEAD
    service: TaskService = Depends(get_task_service),
=======
    service: TaskService = Depends(get_task_service)
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68
):
    return service.get_tasks(skip=skip, limit=limit, completed=completed, search=q)

@router.get("/stats", response_model=TaskStats)
<<<<<<< HEAD
def get_statistics(service: TaskService = Depends(get_task_service)):
    return service.get_statistics()
=======
def stats(service: TaskService = Depends(get_task_service)):
    return service.get_stats()
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, service: TaskService = Depends(get_task_service)):
<<<<<<< HEAD
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
=======
    return service.create_task(task_in)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    task = service.update_task(task_id, task_in)
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68
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
<<<<<<< HEAD
    success = service.delete_task(task_id)
    if not success:
=======
    if not service.delete_task(task_id):
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68
        raise HTTPException(status_code=404, detail="Task not found")