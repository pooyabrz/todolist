from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from src.todolist.domain.models import Task
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.repositories.category_repository import CategoryRepository


class TaskService:
    """
    Service class handling all task-related business logic.
    Acts as an orchestrator between repositories and presentation layer.
    """

    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        Creates instances of required repositories.
        """
        self.db = db
        self.task_repo = TaskRepository(db)
        self.category_repo = CategoryRepository(db)

    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> List[Task]:
        """
        Get a paginated list of tasks with optional filtering and search.
        Categories are eagerly loaded for API responses.
        Used by GET /tasks endpoint.
        """
        return self.task_repo.get_tasks(
            skip=skip,
            limit=limit,
            completed=completed,
            search=search
        )

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a single task by ID with its category eagerly loaded.
        Used by GET /tasks/{task_id}.
        """
        return self.task_repo.get_by_id_with_category(task_id)

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: int = 2,
        due_date: Optional[datetime] = None,
        category_name: Optional[str] = None
    ) -> Task:
        """
        Create a new task with optional category.
        If category_name is provided, it will be created if not exists.
        Returns the created task with category loaded (for API response).
        """
        category_id = None
        if category_name:
            category = self.category_repo.get_or_create(name=category_name.strip())
            category_id = category.id

        # Create the task using repository
        task = self.task_repo.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_id=category_id
        )

        # Re-fetch with category eagerly loaded so it's included in JSON response
        return self.task_repo.get_by_id_with_category(task.id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        due_date: Optional[datetime] = None,
        category_name: Optional[str] = None
    ) -> Optional[Task]:
        """
        Update an existing task.
        Only provided fields are updated.
        Handles category assignment or removal.
        Returns updated task with category loaded, or None if not found.
        """
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None

        update_data: Dict[str, any] = {}

        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if priority is not None:
            update_data['priority'] = priority
        if due_date is not None:
            update_data['due_date'] = due_date

        # Handle category update
        if category_name is not None:
            if category_name.strip():
                category = self.category_repo.get_or_create(name=category_name.strip())
                update_data['category_id'] = category.id
            else:
                update_data['category_id'] = None  # Remove category

        # Perform update
        updated_task = self.task_repo.update(task_id, **update_data)
        if updated_task:
            # Reload with category for consistent API response
            return self.task_repo.get_by_id_with_category(task_id)
        return None

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as completed.
        Sets is_completed=True and completed_at timestamp.
        Returns updated task with category loaded.
        """
        task = self.task_repo.mark_as_completed(task_id)
        if task:
            return self.task_repo.get_by_id_with_category(task_id)
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task permanently.
        Returns True if deleted, False if not found.
        """
        return self.task_repo.delete(task_id)

    def get_statistics(self) -> dict:
        """
        Get current task statistics.
        Used by GET /tasks/stats endpoint.
        """
        return self.task_repo.get_statistics()

    # Legacy methods kept for backward compatibility (CLI, tests, etc.)
    # These were part of Phase 2 and remain unchanged

    def get_all_tasks(self) -> List[Task]:
        """Legacy: Get all tasks with categories (used in CLI)"""
        return self.task_repo.get_all_with_category()

    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks"""
        return self.task_repo.get_by_status(is_completed=False)

    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return self.task_repo.get_by_status(is_completed=True)

    def get_tasks_by_priority(self, priority: int) -> List[Task]:
        """Filter tasks by priority level"""
        return self.task_repo.get_by_priority(priority)

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search in title and description"""
        return self.task_repo.search_tasks(keyword)

    def get_overdue_tasks(self) -> List[Task]:
        """Get tasks past due date and not completed"""
        return self.task_repo.get_overdue_tasks()
    