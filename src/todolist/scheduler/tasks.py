import schedule
import time
from datetime import datetime
from src.todolist.db.session import SessionLocal
from src.todolist.repositories.task_repository import TaskRepository


def close_overdue_tasks():
    """
    Automatically close overdue tasks.
    This function is called periodically by the scheduler.
    """
    db = SessionLocal()
    try:
        repo = TaskRepository(db)
        closed_count = repo.mark_overdue_as_closed()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if closed_count > 0:
            print(f"[{timestamp}] ✅ Closed {closed_count} overdue task(s)")
        else:
            print(f"[{timestamp}] ℹ️  No overdue tasks to close")
            
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ❌ Error in scheduler: {e}")
    finally:
        db.close()


def run_scheduler():
    """
    Run the task scheduler.
    This function runs in a separate process and executes scheduled tasks.
    """
    print("🚀 Task Scheduler started...")
    print("⏰ Schedule: Check overdue tasks every 15 minutes")
    print("=" * 50)
    
    # Schedule the task to run every 15 minutes
    schedule.every(15).minutes.do(close_overdue_tasks)
    
    # Alternative schedules (commented out):
    # schedule.every().day.at("02:00").do(close_overdue_tasks)  # Daily at 2 AM
    # schedule.every().hour.do(close_overdue_tasks)  # Every hour
    
    # Run immediately for testing
    close_overdue_tasks()
    
    # Main scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds


if __name__ == "__main__":
    run_scheduler()
