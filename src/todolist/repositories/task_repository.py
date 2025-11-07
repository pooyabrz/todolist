from typing import List, Optional
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from todolist.domain.models import Task
from .base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Repository for Task entity with specialized methods.
    """
    
    def __init__(self, db: Session):
        """
        Initialize task repository.
        
        Args:
            db: Database session
        """
        super().__init__(Task, db)
    
    def get_all_with_category(self) -> List[Task]:
        """
        Get all tasks with their categories eagerly loaded.
        
        Returns:
            List of tasks with categories
        """
        return self.db.query(Task).options(joinedload(Task.category)).all()
    
    def get_by_status(self, is_completed: bool) -> List[Task]:
        """
        Get tasks filtered by completion status.
        
        Args:
            is_completed: True for completed, False for pending
            
        Returns:
            List of filtered tasks
        """
        return self.db.query(Task).filter(Task.is_completed == is_completed).all()
    
    def get_by_priority(self, priority: int) -> List[Task]:
        """
        Get tasks filtered by priority.
        
        Args:
            priority: Priority level (1=Low, 2=Medium, 3=High)
            
        Returns:
            List of tasks with specified priority
        """
        return self.db.query(Task).filter(Task.priority == priority).all()
    
    def get_by_category(self, category_id: int) -> List[Task]:
        """
        Get tasks by category.
        
        Args:
            category_id: Category ID
            
        Returns:
            List of tasks in category
        """
        return self.db.query(Task).filter(Task.category_id == category_id).all()
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks (not completed and due date passed).
        
        Returns:
            List of overdue tasks
        """
        now = datetime.utcnow()
        return self.db.query(Task).filter(
            Task.is_completed == False,
            Task.due_date < now
        ).all()
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching tasks
        """
        search_pattern = f"%{keyword}%"
        return self.db.query(Task).filter(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        ).all()
    
    def mark_as_completed(self, task_id: int) -> Optional[Task]:
        """
        Mark task as completed.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task or None if not found
        """
        task = self.get_by_id(task_id)
        if task and not task.is_completed:
            task.is_completed = True
            task.completed_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(task)
        return task
    
    def mark_overdue_as_closed(self) -> int:
        """
        Mark all overdue tasks as completed.
        Used by scheduler for automatic task closure.
        
        Returns:
            Number of tasks closed
        """
        overdue_tasks = self.get_overdue_tasks()
        count = 0
        
        for task in overdue_tasks:
            task.is_completed = True
            task.completed_at = datetime.utcnow()
            count += 1
        
        if count > 0:
            self.db.commit()
        
        return count
    
    def get_statistics(self) -> dict:
        """
        Get task statistics.
        
        Returns:
            Dictionary with task counts
        """
        total = self.count()
        completed = self.db.query(Task).filter(Task.is_completed == True).count()
        pending = total - completed
        overdue = len(self.get_overdue_tasks())
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue
        }
