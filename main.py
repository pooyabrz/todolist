from fastapi import FastAPI
from src.todolist.api.routers.task_router import router as task_router

app = FastAPI(
    title="To Do List Project (Phase 3 - Web API)",
    description="FastAPI",
<<<<<<< HEAD
    version="3.0.0",
=======
    version="1.0.0",
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "Welcome to ToDoList Web API - Phase 3"}