import sys
from src.todolist.db.session import SessionLocal
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.scheduler.tasks import run_scheduler, close_overdue_tasks


def run_autoclose_once():
    """
    Run overdue task closure once (not continuous).
    Provides interactive confirmation before closing tasks.
    """
    print("🔍 Checking for overdue tasks...")
    
    db = SessionLocal()
    try:
        repo = TaskRepository(db)
        overdue_tasks = repo.get_overdue_tasks()
        
        if not overdue_tasks:
            print("✅ No overdue tasks found!")
            return
        
        print(f"📋 Found {len(overdue_tasks)} overdue task(s):")
        for task in overdue_tasks:
            print(f"  - [{task.id}] {task.title} (Due: {task.due_date})")
        
        # Ask for user confirmation
        confirm = input("\n❓ Do you want to close these tasks? (y/n): ")
        
        if confirm.lower() == 'y':
            closed_count = repo.mark_overdue_as_closed()
            print(f"\n✅ Successfully closed {closed_count} task(s)!")
        else:
            print("\n❌ Operation cancelled.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        db.close()


def run_autoclose_daemon():
    """
    Run scheduler in daemon mode (continuous background operation).
    Runs the scheduler that checks for overdue tasks every 15 minutes.
    """
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\n\n⏹️  Scheduler stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Scheduler error: {e}")
        sys.exit(1)


def handle_autoclose_command(args):
    """
    Handle the autoclose command.
    
    Usage:
        todolist tasks:autoclose-overdue           # Run once
        todolist tasks:autoclose-overdue --daemon  # Run continuously
        todolist tasks:autoclose-overdue -d        # Run continuously (short form)
    
    Args:
        args: Command-line arguments
    """
    if '--daemon' in args or '-d' in args:
        run_autoclose_daemon()
    else:
        run_autoclose_once()
