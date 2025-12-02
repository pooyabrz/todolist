from fastapi import FastAPI
from src.todolist.api.routers.task_router import router as task_router

app = FastAPI(
    title="To Do List Project (Phase 3 - Web API)",
    description="FastAPI",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "Welcome to ToDoList Web API - Phase 3"}