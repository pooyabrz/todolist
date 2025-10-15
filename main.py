from typing import Optional
from datetime import datetime
from src.todolist.infrastructure.repository import InMemoryRepository
from src.todolist.application.services import ProjectService, TaskService


def print_project(project):
    """Print project details."""
    print(f"ID: {project.id}, Name: {project.name}, Description: {project.description}")


def print_task(task):
    """Print task details."""
    deadline_str = task.deadline.isoformat() if task.deadline else "None"
    print(
        f"ID: {task.id}, Title: {task.title}, Status: {task.status.value}, Deadline: {deadline_str}"
    )


def main():
    """Main CLI loop."""
    repo = InMemoryRepository()
    project_service = ProjectService(repo)
    task_service = TaskService(repo)

    commands = {
        "create_project": "Create a new project: name description",
        "edit_project": "Edit project: project_id [name] [description]",
        "delete_project": "Delete project: project_id",
        "list_projects": "List all projects",
        "add_task": "Add task to project: project_id title [description] [status] [deadline]",
        "change_task_status": "Change task status: project_id task_id new_status",
        "edit_task": "Edit task: project_id task_id [title] [description] [deadline]",
        "delete_task": "Delete task: project_id task_id",
        "list_tasks": "List tasks for project: project_id",
        "help": "Show this help",
        "exit": "Exit the application",
    }

    print("Welcome to ToDoList CLI. Type 'help' for commands.")

    while True:
        input_str = input("> ").strip()
        if not input_str:
            continue
        parts = input_str.split()
        cmd = parts[0]

        try:
            if cmd == "create_project":
                name = parts[1]
                desc = " ".join(parts[2:]) if len(parts) > 2 else ""
                project = project_service.create_project(name, desc)
                print("Project created:")
                print_project(project)

            elif cmd == "edit_project":
                project_id = int(parts[1])
                name = parts[2] if len(parts) > 2 else None
                desc = " ".join(parts[3:]) if len(parts) > 3 else None
                project = project_service.edit_project(project_id, name, desc)
                if project:
                    print("Project updated:")
                    print_project(project)
                else:
                    print("Project not found.")

            elif cmd == "delete_project":
                project_id = int(parts[1])
                if project_service.delete_project(project_id):
                    print("Project deleted.")
                else:
                    print("Project not found.")

            elif cmd == "list_projects":
                projects = project_service.list_projects()
                if not projects:
                    print("No projects found.")
                for p in projects:
                    print_project(p)

            elif cmd == "add_task":
                project_id = int(parts[1])
                title = parts[2]
                desc = parts[3] if len(parts) > 3 else ""
                status = parts[4] if len(parts) > 4 else "todo"
                deadline = parts[5] if len(parts) > 5 else None
                task = task_service.add_task(project_id, title, desc, status, deadline)
                if task:
                    print("Task added:")
                    print_task(task)
                else:
                    print("Project not found.")

            elif cmd == "change_task_status":
                project_id = int(parts[1])
                task_id = int(parts[2])
                new_status = parts[3]
                if task_service.change_task_status(project_id, task_id, new_status):
                    print("Task status updated.")
                else:
                    print("Task or project not found, or invalid status.")

            elif cmd == "edit_task":
                project_id = int(parts[1])
                task_id = int(parts[2])
                title = parts[3] if len(parts) > 3 else None
                desc = parts[4] if len(parts) > 4 else None
                deadline = parts[5] if len(parts) > 5 else None
                task = task_service.edit_task(
                    project_id, task_id, title, desc, deadline
                )
                if task:
                    print("Task updated:")
                    print_task(task)
                else:
                    print("Task or project not found.")

            elif cmd == "delete_task":
                project_id = int(parts[1])
                task_id = int(parts[2])
                if task_service.delete_task(project_id, task_id):
                    print("Task deleted.")
                else:
                    print("Task or project not found.")

            elif cmd == "list_tasks":
                project_id = int(parts[1])
                tasks = task_service.list_tasks(project_id)
                if not tasks:
                    print("No tasks found or project not exists.")
                for t in tasks:
                    print_task(t)

            elif cmd == "help":
                for c, desc in commands.items():
                    print(f"{c}: {desc}")

            elif cmd == "exit":
                break

            else:
                print("Unknown command. Type 'help' for list.")

        except ValueError as e:
            print(f"Error: {e}")
        except IndexError:
            print("Invalid arguments. Check 'help'.")


if __name__ == "__main__":
    main()
