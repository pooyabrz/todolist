from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from todolist.domain.models import Task
from todolist.repositories.task_repository import TaskRepository
from todolist.repositories.category_repository import CategoryRepository


class TaskService:
    """
    Service class for task-related business logic.
    Orchestrates operations between repositories.
    """
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: Database session
        """
        self.db = db
        self.task_repo = TaskRepository(db)
        self.category_repo = CategoryRepository(db)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks with their categories.
        
        Returns:
            List of all tasks
        """
        return self.task_repo.get_all_with_category()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task or None if not found
        """
        return self.task_repo.get_by_id(task_id)
    
    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: int = 2,
        due_date: Optional[datetime] = None,
        category_name: Optional[str] = None
    ) -> Task:
        """
        Create a new task.
        
        Args:
            title: Task title
            description: Task description (optional)
            priority: Priority level 1-3 (default: 2)
            due_date: Due date (optional)
            category_name: Category name (optional)
            
        Returns:
            Created task
        """
        # Handle category
        category_id = None
        if category_name:
            category = self.category_repo.get_or_create(name=category_name)
            category_id = category.id
        
        # Create task
        task = self.task_repo.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_id=category_id
        )
        
        return task
    
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
        
        Args:
            task_id: Task ID
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            due_date: New due date (optional)
            category_name: New category name (optional)
            
        Returns:
            Updated task or None if not found
        """
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        # Prepare update data
        update_data = {}
        
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if priority is not None:
            update_data['priority'] = priority
        if due_date is not None:
            update_data['due_date'] = due_date
        
        # Handle category
        if category_name is not None:
            if category_name:
                category = self.category_repo.get_or_create(name=category_name)
                update_data['category_id'] = category.id
            else:
                update_data['category_id'] = None
        
        # Update task
        return self.task_repo.update(task_id, **update_data)
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if deleted, False if not found
        """
        return self.task_repo.delete(task_id)
    
    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark task as completed.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task or None if not found
        """
        return self.task_repo.mark_as_completed(task_id)
    
    def get_pending_tasks(self) -> List[Task]:
        """
        Get all pending (incomplete) tasks.
        
        Returns:
            List of pending tasks
        """
        return self.task_repo.get_by_status(is_completed=False)
    
    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.
        
        Returns:
            List of completed tasks
        """
        return self.task_repo.get_by_status(is_completed=True)
    
    def get_tasks_by_priority(self, priority: int) -> List[Task]:
        """
        Get tasks by priority level.
        
        Args:
            priority: Priority level (1-3)
            
        Returns:
            List of tasks with specified priority
        """
        return self.task_repo.get_by_priority(priority)
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching tasks
        """
        return self.task_repo.search_tasks(keyword)
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks.
        
        Returns:
            List of overdue tasks
        """
        return self.task_repo.get_overdue_tasks()
    
    def get_statistics(self) -> dict:
        """
        Get task statistics.
        
        Returns:
            Dictionary with statistics
        """
        return self.task_repo.get_statistics()
