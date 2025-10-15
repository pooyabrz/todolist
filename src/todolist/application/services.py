from typing import List, Optional
from datetime import datetime
from todolist.domain.models import Project, Task
from todolist.infrastructure.repository import InMemoryRepository


class ProjectService:
    """Service for managing projects."""

    def __init__(self, repo: InMemoryRepository):
        self.repo = repo

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project."""
        return self.repo.create_project(name, description)

    def edit_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Project]:
        """Edit an existing project."""
        return self.repo.update_project(project_id, name, description)

    def delete_project(self, project_id: int) -> bool:
        """Delete a project."""
        return self.repo.delete_project(project_id)

    def list_projects(self) -> List[Project]:
        """List all projects."""
        return self.repo.list_projects()


class TaskService:
    """Service for managing tasks."""

    def __init__(self, repo: InMemoryRepository):
        self.repo = repo

    def add_task(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: str = "todo",
        deadline: Optional[str] = None,
    ) -> Optional[Task]:
        """Add a task to a project.

        Args:
            deadline: ISO format string for deadline.
        """
        deadline_dt = datetime.fromisoformat(deadline) if deadline else None
        return self.repo.add_task_to_project(
            project_id, title, description, status, deadline_dt
        )

    def change_task_status(
        self, project_id: int, task_id: int, new_status: str
    ) -> bool:
        """Change the status of a task."""
        return bool(self.repo.update_task(project_id, task_id, status=new_status))

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> Optional[Task]:
        """Edit a task's details (excluding status)."""
        deadline_dt = datetime.fromisoformat(deadline) if deadline else None
        return self.repo.update_task(
            project_id, task_id, title, description, deadline=deadline_dt
        )

    def delete_task(self, project_id: int, task_id: int) -> bool:
        """Delete a task."""
        return self.repo.delete_task(project_id, task_id)

    def list_tasks(self, project_id: int) -> List[Task]:
        """List tasks for a project."""
        return self.repo.list_tasks(project_id)
