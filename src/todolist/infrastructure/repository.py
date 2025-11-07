from typing import Dict, List, Optional
from datetime import datetime
from src.todolist.domain.models import Project, Task, TaskStatus
from src.todolist.config import Config


class InMemoryRepository:
    """In-memory storage implementation for projects and tasks."""

    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self.next_project_id: int = 1
        self.next_task_id: int = 1

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project.

        Args:
            name: Name of the project.
            description: Optional description.

        Returns:
            The created project.

        Raises:
            ValueError: If max projects limit is reached or validation fails.
        """
        if len(self.projects) >= Config.MAX_PROJECTS:
            raise ValueError("Max projects limit reached")
        if any(p.name == name for p in self.projects.values()):
            raise ValueError("Project name already exists")
        project = Project(self.next_project_id, name, description)
        self.projects[self.next_project_id] = project
        self.next_project_id += 1
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by ID.

        Args:
            project_id: ID of the project.

        Returns:
            The project if found, else None.
        """
        return self.projects.get(project_id)

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Project]:
        """Update a project's name or description.

        Args:
            project_id: ID of the project.
            name: New name (optional).
            description: New description (optional).

        Returns:
            The updated project if found, else None.

        Raises:
            ValueError: If new name is duplicate or validation fails.
        """
        project = self.get_project(project_id)
        if not project:
            return None
        if name:
            if len(name.split()) > 30:
                raise ValueError("Name exceeds 30 words")
            if any(
                p.name == name and p.id != project_id for p in self.projects.values()
            ):
                raise ValueError("Project name already exists")
            project.name = name
        if description:
            if len(description.split()) > 150:
                raise ValueError("Description exceeds 150 words")
            project.description = description
        return project

    def delete_project(self, project_id: int) -> bool:
        """Delete a project and its associated tasks (cascade delete).

        Args:
            project_id: ID of the project.

        Returns:
            True if deleted, False otherwise.
        """
        if project_id in self.projects:
            del self.projects[project_id]
            return True
        return False

    def list_projects(self) -> List[Project]:
        """List all projects.

        Returns:
            List of all projects.
        """
        return sorted(list(self.projects.values()), key=lambda p: p.id)

    def add_task_to_project(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: str = "todo",
        deadline: Optional[datetime] = None,
    ) -> Optional[Task]:
        """Add a new task to a project.

        Args:
            project_id: ID of the project.
            title: Title of the task.
            description: Optional description.
            status: Status of the task (default 'todo').
            deadline: Optional deadline.

        Returns:
            The created task if project found, else None.

        Raises:
            ValueError: If max tasks limit reached, invalid status, or validation fails.
        """
        project = self.get_project(project_id)
        if not project:
            return None
        if len(project.tasks) >= Config.MAX_TASKS_PER_PROJECT:
            raise ValueError("Max tasks limit reached for project")
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise ValueError("Invalid task status")
        task = Task(self.next_task_id, title, description, task_status, deadline)
        project.tasks.append(task)
        self.next_task_id += 1
        return task

    def get_task(self, project_id: int, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID within a project.

        Args:
            project_id: ID of the project.
            task_id: ID of the task.

        Returns:
            The task if found, else None.
        """
        project = self.get_project(project_id)
        if not project:
            return None
        return next((t for t in project.tasks if t.id == task_id), None)

    def update_task(
        self,
        project_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> Optional[Task]:
        """Update a task's details.

        Args:
            project_id: ID of the project.
            task_id: ID of the task.
            title: New title (optional).
            description: New description (optional).
            status: New status (optional).
            deadline: New deadline (optional).

        Returns:
            The updated task if found, else None.

        Raises:
            ValueError: If invalid status or validation fails.
        """
        task = self.get_task(project_id, task_id)
        if not task:
            return None
        if title:
            if len(title.split()) > 30:
                raise ValueError("Title exceeds 30 words")
            task.title = title
        if description:
            if len(description.split()) > 150:
                raise ValueError("Description exceeds 150 words")
            task.description = description
        if status:
            try:
                task.status = TaskStatus(status)
            except ValueError:
                raise ValueError("Invalid task status")
        if deadline is not None:
            if deadline and deadline < datetime.now():
                raise ValueError("Deadline must be in the future")
            task.deadline = deadline
        return task

    def delete_task(self, project_id: int, task_id: int) -> bool:
        """Delete a task from a project.

        Args:
            project_id: ID of the project.
            task_id: ID of the task.

        Returns:
            True if deleted, False otherwise.
        """
        project = self.get_project(project_id)
        if not project:
            return False
        task = self.get_task(project_id, task_id)
        if task:
            project.tasks.remove(task)
            return True
        return False

    def list_tasks(self, project_id: int) -> List[Task]:
        """List all tasks for a project.

        Args:
            project_id: ID of the project.

        Returns:
            List of tasks if project found, else empty list.
        """
        project = self.get_project(project_id)
        return sorted(project.tasks, key=lambda t: t.id) if project else []
