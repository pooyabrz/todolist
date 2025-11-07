from typing import Optional
from sqlalchemy.orm import Session
from todolist.domain.models import Category
from .base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Repository for Category entity.
    """
    
    def __init__(self, db: Session):
        """
        Initialize category repository.
        
        Args:
            db: Database session
        """
        super().__init__(Category, db)
    
    def get_by_name(self, name: str) -> Optional[Category]:
        """
        Get category by name.
        
        Args:
            name: Category name
            
        Returns:
            Category or None if not found
        """
        return self.db.query(Category).filter(Category.name == name).first()
    
    def get_or_create(self, name: str, description: str = None) -> Category:
        """
        Get existing category or create new one if doesn't exist.
        
        Args:
            name: Category name
            description: Category description (optional)
            
        Returns:
            Existing or newly created category
        """
        category = self.get_by_name(name)
        
        if not category:
            category = self.create(name=name, description=description)
        
        return category
    
    def get_with_task_count(self):
        """
        Get all categories with their task count.
        
        Returns:
            List of tuples (category, task_count)
        """
        from sqlalchemy import func
        from app.domain.models import Task
        
        result = self.db.query(
            Category,
            func.count(Task.id).label('task_count')
        ).outerjoin(Task).group_by(Category.id).all()
        
        return result
