from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from src.todolist.db.session import Base

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository class with common database operations.
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository with model and database session.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get entity by ID.
        
        Args:
            id: Entity ID
            
        Returns:
            Entity or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self) -> List[ModelType]:
        """
        Get all entities.
        
        Returns:
            List of all entities
        """
        return self.db.query(self.model).all()
    
    def create(self, **kwargs) -> ModelType:
        """
        Create new entity.
        
        Args:
            **kwargs: Entity attributes
            
        Returns:
            Created entity
        """
        entity = self.model(**kwargs)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """
        Update entity by ID.
        
        Args:
            id: Entity ID
            **kwargs: Attributes to update
            
        Returns:
            Updated entity or None if not found
        """
        entity = self.get_by_id(id)
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            self.db.commit()
            self.db.refresh(entity)
        return entity
    
    def delete(self, id: int) -> bool:
        """
        Delete entity by ID.
        
        Args:
            id: Entity ID
            
        Returns:
            True if deleted, False if not found
        """
        entity = self.get_by_id(id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        """
        Count total entities.
        
        Returns:
            Total count
        """
        return self.db.query(self.model).count()
