from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Enumeration for task statuses."""

    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Task:
    """Represents a task within a project.

    Attributes:
        id: Unique identifier for the task.
        title: Title of the task (max 30 words).
        description: Description of the task (max 150 words).
        status: Current status of the task.
        deadline: Optional deadline for the task.
    """

    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    deadline: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization validation."""
        if len(self.title.split()) > 30:
            raise ValueError("Title exceeds 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Description exceeds 150 words")
        if self.deadline and self.deadline < datetime.now():
            raise ValueError("Deadline must be in the future")


@dataclass
class Project:
    """Represents a project containing multiple tasks.

    Attributes:
        id: Unique identifier for the project.
        name: Name of the project (max 30 words).
        description: Description of the project (max 150 words).
        tasks: List of tasks associated with the project.
    """

    id: int
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Post-initialization validation."""
        if len(self.name.split()) > 30:
            raise ValueError("Name exceeds 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Description exceeds 150 words")
