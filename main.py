"""
Main entry point for the ToDoList application.
"""
import sys
from datetime import datetime
from src.todolist.db.session import check_database_connection, SessionLocal
from src.todolist.services.task_service import TaskService
from src.todolist.cli.scheduler_cli import handle_autoclose_command


def print_help():
    """Print usage help information."""
    help_text = """
📝 ToDoList - Task Management Application

Usage: python main.py <command> [options]

Commands:
  tasks:list                    List all tasks
  tasks:create                  Create a new task (interactive)
  tasks:show <id>              Show task details
  tasks:update <id>            Update a task
  tasks:delete <id>            Delete a task
  tasks:complete <id>          Mark task as completed
  tasks:search <keyword>       Search tasks by keyword
  tasks:stats                  Show task statistics
  tasks:pending                Show pending tasks
  tasks:completed              Show completed tasks
  tasks:overdue                Show overdue tasks
  
  tasks:autoclose-overdue      Close overdue tasks once
  tasks:autoclose-overdue -d   Run scheduler in daemon mode
  
  db:check                     Check database connection
  help                         Show this help message

Examples:
  python main.py tasks:list
  python main.py tasks:create
  python main.py tasks:complete 5
  python main.py tasks:autoclose-overdue --daemon
"""
    print(help_text)


def handle_tasks_list():
    """Display list of all tasks."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        tasks = service.get_all_tasks()
        
        if not tasks:
            print("📭 No tasks found!")
            return
        
        print(f"\n📋 All Tasks ({len(tasks)} total):\n")
        print(f"{'ID':<5} {'Title':<30} {'Status':<12} {'Priority':<10} {'Due Date':<20}")
        print("=" * 85)
        
        for task in tasks:
            status = "✅ Done" if task.is_completed else "⏳ Pending"
            priority_map = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}
            priority = priority_map.get(task.priority, "Unknown")
            due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "N/A"
            
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            print(f"{task.id:<5} {title:<30} {status:<12} {priority:<10} {due:<20}")
            
    finally:
        db.close()


def handle_tasks_create():
    """Create a new task interactively."""
    print("\n📝 Create New Task\n")
    
    # Get task details from user
    title = input("Title: ").strip()
    if not title:
        print("❌ Title is required!")
        return
    
    description = input("Description (optional): ").strip() or None
    
    # Get priority
    print("\nPriority:")
    print("  1. 🟢 Low")
    print("  2. 🟡 Medium")
    print("  3. 🔴 High")
    priority_input = input("Select priority (1-3, default 2): ").strip()
    priority = int(priority_input) if priority_input in ['1', '2', '3'] else 2
    
    # Get due date
    due_date_str = input("Due date (YYYY-MM-DD HH:MM, optional): ").strip()
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("⚠️  Invalid date format, skipping due date...")
    
    # Get category
    category = input("Category (optional): ").strip() or None
    
    # Create task
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.create_task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_name=category
        )
        print(f"\n✅ Task created successfully! (ID: {task.id})")
    except Exception as e:
        print(f"\n❌ Error creating task: {e}")
    finally:
        db.close()


def handle_tasks_show(task_id: int):
    """Show detailed information about a task."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.get_task_by_id(task_id)
        
        if not task:
            print(f"❌ Task with ID {task_id} not found!")
            return
        
        print(f"\n📋 Task Details:\n")
        print(f"ID:           {task.id}")
        print(f"Title:        {task.title}")
        print(f"Description:  {task.description or 'N/A'}")
        print(f"Status:       {'✅ Completed' if task.is_completed else '⏳ Pending'}")
        
        priority_map = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}
        print(f"Priority:     {priority_map.get(task.priority, 'Unknown')}")
        
        print(f"Category:     {task.category.name if task.category else 'N/A'}")
        print(f"Due Date:     {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'N/A'}")
        print(f"Created:      {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        if task.is_completed and task.completed_at:
            print(f"Completed:    {task.completed_at.strftime('%Y-%m-%d %H:%M')}")
        
        if task.is_overdue:
            print(f"\n⚠️  This task is OVERDUE!")
            
    finally:
        db.close()


def handle_tasks_update(task_id: int):
    """Update an existing task."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.get_task_by_id(task_id)
        
        if not task:
            print(f"❌ Task with ID {task_id} not found!")
            return
        
        print(f"\n✏️  Update Task (ID: {task_id})")
        print("Leave blank to keep current value\n")
        
        # Get new values
        title = input(f"Title [{task.title}]: ").strip() or None
        description = input(f"Description [{task.description or 'N/A'}]: ").strip() or None
        
        # Priority
        priority_map = {1: "Low", 2: "Medium", 3: "High"}
        current_priority = priority_map.get(task.priority, "Unknown")
        priority_input = input(f"Priority (1-3) [{current_priority}]: ").strip()
        priority = int(priority_input) if priority_input in ['1', '2', '3'] else None
        
        # Due date
        current_due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "N/A"
        due_date_str = input(f"Due date (YYYY-MM-DD HH:MM) [{current_due}]: ").strip()
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("⚠️  Invalid date format, keeping current due date...")
        
        # Category
        current_category = task.category.name if task.category else "N/A"
        category = input(f"Category [{current_category}]: ").strip() or None
        
        # Update task
        updated_task = service.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_name=category
        )
        
        if updated_task:
            print(f"\n✅ Task updated successfully!")
        else:
            print(f"\n❌ Failed to update task!")
            
    except Exception as e:
        print(f"\n❌ Error updating task: {e}")
    finally:
        db.close()


def handle_tasks_delete(task_id: int):
    """Delete a task."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.get_task_by_id(task_id)
        
        if not task:
            print(f"❌ Task with ID {task_id} not found!")
            return
        
        print(f"\n⚠️  You are about to delete:")
        print(f"    [{task.id}] {task.title}")
        
        confirm = input("\nAre you sure? (y/n): ")
        
        if confirm.lower() == 'y':
            if service.delete_task(task_id):
                print(f"\n✅ Task deleted successfully!")
            else:
                print(f"\n❌ Failed to delete task!")
        else:
            print("\n❌ Deletion cancelled.")
            
    finally:
        db.close()


def handle_tasks_complete(task_id: int):
    """Mark a task as completed."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.complete_task(task_id)
        
        if task:
            print(f"✅ Task '{task.title}' marked as completed!")
        else:
            print(f"❌ Task with ID {task_id} not found!")
            
    finally:
        db.close()


def handle_tasks_search(keyword: str):
    """Search tasks by keyword."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        tasks = service.search_tasks(keyword)
        
        if not tasks:
            print(f"📭 No tasks found matching '{keyword}'")
            return
        
        print(f"\n🔍 Search Results ({len(tasks)} found):\n")
        print(f"{'ID':<5} {'Title':<30} {'Status':<12} {'Priority':<10}")
        print("=" * 65)
        
        for task in tasks:
            status = "✅ Done" if task.is_completed else "⏳ Pending"
            priority_map = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}
            priority = priority_map.get(task.priority, "Unknown")
            
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            print(f"{task.id:<5} {title:<30} {status:<12} {priority:<10}")
            
    finally:
        db.close()


def handle_tasks_stats():
    """Display task statistics."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        stats = service.get_statistics()
        
        print("\n📊 Task Statistics:\n")
        print(f"Total Tasks:      {stats['total']}")
        print(f"✅ Completed:     {stats['completed']}")
        print(f"⏳ Pending:       {stats['pending']}")
        print(f"⚠️  Overdue:       {stats['overdue']}")
        
        if stats['total'] > 0:
            completion_rate = (stats['completed'] / stats['total']) * 100
            print(f"\nCompletion Rate:  {completion_rate:.1f}%")
            
    finally:
        db.close()


def handle_tasks_pending():
    """Display pending tasks."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        tasks = service.get_pending_tasks()
        
        if not tasks:
            print("✅ No pending tasks!")
            return
        
        print(f"\n⏳ Pending Tasks ({len(tasks)}):\n")
        print(f"{'ID':<5} {'Title':<30} {'Priority':<10} {'Due Date':<20}")
        print("=" * 70)
        
        for task in tasks:
            priority_map = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}
            priority = priority_map.get(task.priority, "Unknown")
            due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "N/A"
            
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            print(f"{task.id:<5} {title:<30} {priority:<10} {due:<20}")
            
    finally:
        db.close()


def handle_tasks_completed():
    """Display completed tasks."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        tasks = service.get_completed_tasks()
        
        if not tasks:
            print("📭 No completed tasks!")
            return
        
        print(f"\n✅ Completed Tasks ({len(tasks)}):\n")
        print(f"{'ID':<5} {'Title':<30} {'Completed At':<20}")
        print("=" * 60)
        
        for task in tasks:
            completed = task.completed_at.strftime("%Y-%m-%d %H:%M") if task.completed_at else "Unknown"
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            print(f"{task.id:<5} {title:<30} {completed:<20}")
            
    finally:
        db.close()


def handle_tasks_overdue():
    """Display overdue tasks."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        tasks = service.get_overdue_tasks()
        
        if not tasks:
            print("✅ No overdue tasks!")
            return
        
        print(f"\n⚠️  Overdue Tasks ({len(tasks)}):\n")
        print(f"{'ID':<5} {'Title':<30} {'Due Date':<20} {'Priority':<10}")
        print("=" * 70)
        
        for task in tasks:
            priority_map = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}
            priority = priority_map.get(task.priority, "Unknown")
            due = task.due_date.strftime("%Y-%m-%d %H:%M")
            
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            print(f"{task.id:<5} {title:<30} {due:<20} {priority:<10}")
            
    finally:
        db.close()


def main():
    """Main application entry point."""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    try:
        # Database check command
        if command == "db:check":
            check_database_connection()
        
        # Help command
        elif command == "help":
            print_help()
        
        # Task commands
        elif command == "tasks:list":
            handle_tasks_list()
        
        elif command == "tasks:create":
            handle_tasks_create()
        
        elif command == "tasks:show":
            if len(sys.argv) < 3:
                print("❌ Usage: python main.py tasks:show <id>")
                sys.exit(1)
            handle_tasks_show(int(sys.argv[2]))
        
        elif command == "tasks:update":
            if len(sys.argv) < 3:
                print("❌ Usage: python main.py tasks:update <id>")
                sys.exit(1)
            handle_tasks_update(int(sys.argv[2]))
        
        elif command == "tasks:delete":
            if len(sys.argv) < 3:
                print("❌ Usage: python main.py tasks:delete <id>")
                sys.exit(1)
            handle_tasks_delete(int(sys.argv[2]))
        
        elif command == "tasks:complete":
            if len(sys.argv) < 3:
                print("❌ Usage: python main.py tasks:complete <id>")
                sys.exit(1)
            handle_tasks_complete(int(sys.argv[2]))
        
        elif command == "tasks:search":
            if len(sys.argv) < 3:
                print("❌ Usage: python main.py tasks:search <keyword>")
                sys.exit(1)
            handle_tasks_search(sys.argv[2])
        
        elif command == "tasks:stats":
            handle_tasks_stats()
        
        elif command == "tasks:pending":
            handle_tasks_pending()
        
        elif command == "tasks:completed":
            handle_tasks_completed()
        
        elif command == "tasks:overdue":
            handle_tasks_overdue()
        
        # Scheduler command
        elif command == "tasks:autoclose-overdue":
            handle_autoclose_command(sys.argv[2:])
        
        else:
            print(f"❌ Unknown command: {command}")
            print("Run 'python main.py help' for usage information.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
