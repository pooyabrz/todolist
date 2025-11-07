from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from todolist.db.session import Base


class Category(Base):
    """
    Category model for task categorization.
    """
    __tablename__ = 'categories'
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Category attributes
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tasks = relationship(
        "Task",
        back_populates="category",
        cascade="all, delete-orphan",  # Delete tasks when category is deleted
        lazy="dynamic"  # Load tasks on demand
    )
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Task(Base):
    """
    Task model representing a todo item.
    """
    __tablename__ = 'tasks'
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Task attributes
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=2, nullable=False)  # 1=Low, 2=Medium, 3=High
    is_completed = Column(Boolean, default=False, nullable=False, index=True)
    
    # Dates
    due_date = Column(DateTime, nullable=True, index=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="tasks")
    
    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_task_status_priority', 'is_completed', 'priority'),
        Index('idx_task_due_date_status', 'due_date', 'is_completed'),
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.is_completed})>"
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and not self.is_completed:
            return datetime.utcnow() > self.due_date
        return False
