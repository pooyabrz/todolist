from typing import List, Optional
from datetime import datetime
from todolist.domain.models import Project, Task, TaskStatus
from todolist.infrastructure.repository import InMemoryRepository

class ProjectService:
    """Business logic for projects."""
    def __init__(self, repo: InMemoryRepository):
        self.repo = repo

    def create_project(self, name: str, description: str = "") -> Project:
        return self.repo.create_project(name, description)

    def edit_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Project]:
        return self.repo.update_project(project_id, name, description)

    def delete_project(self, project_id: int) -> bool:
        return self.repo.delete_project(project_id)

    def list_projects(self) -> List[Project]:
        return self.repo.list_projects()

class TaskService:
    """Business logic for tasks."""
    def __init__(self, repo: InMemoryRepository):
        self.repo = repo

    def add_task(self, project_id: int, title: str, description: str = "", status: str = "todo", deadline: Optional[str] = None) -> Optional[Task]:
        deadline_dt = datetime.fromisoformat(deadline) if deadline else None
        return self.repo.add_task_to_project(project_id, title, description, status, deadline_dt)

    def change_task_status(self, project_id: int, task_id: int, new_status: str) -> bool:
        # Implementation: find task, update status if valid
        project = self.repo.get_project(project_id)
        if not project:
            return False
        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            return False
        try:
            task.status = TaskStatus(new_status)
            return True
        except ValueError:
            return False
