from typing import Dict, Optional
from src.todolist.domain.models import Project, Task
from src.todolist.config import Config

class InMemoryRepository:
    """In-memory storage for projects and tasks."""
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self.next_project_id: int = 1
        self.next_task_id: int = 1

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self.projects) >= Config.MAX_PROJECTS:
            raise ValueError("Max projects limit reached")
        project = Project(self.next_project_id, name, description)
        self.projects[self.next_project_id] = project
        self.next_project_id += 1
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.projects.get(project_id)

    def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Project]:
        project = self.get_project(project_id)
        if not project:
            return None
        if name:
            if any(p.name == name and p.id != project_id for p in self.projects.values()):
                raise ValueError("Project name already exists")
            project.name = name
        if description:
            project.description = description
        return project

    def delete_project(self, project_id: int) -> bool:
        if project_id in self.projects:
            del self.projects[project_id]  # Cascade delete: tasks are in project.tasks, so auto-deleted
            return True
        return False

    def list_projects(self) -> List[Project]:
        return list(self.projects.values())

    def add_task_to_project(self, project_id: int, title: str, description: str = "", status: str = "todo", deadline: Optional[datetime] = None) -> Optional[Task]:
        project = self.get_project(project_id)
        if not project:
            return None
        if len(project.tasks) >= Config.MAX_TASKS_PER_PROJECT:
            raise ValueError("Max tasks limit reached for project")
        task_status = TaskStatus(status)
        task = Task(self.next_task_id, title, description, task_status, deadline)
        project.tasks.append(task)
        self.next_task_id += 1
        return task
