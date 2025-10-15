# To Do List Project (Phase 1 - In-Memory)

**Prepared for:** Software Engineering Course, AUT  
**Date:** October 2025  
**Version:** 1.0.0

## 📋 Project Overview

A Python-based ToDoList application built with Object-Oriented Programming principles and in-memory storage. This initial phase delivers a fully functional command-line application that demonstrates clean architecture, proper separation of concerns, and adherence to Python best practices.

### 🎯 Key Objectives
- Implement core project and task management functionalities
- Demonstrate clean architecture with layered design
- Apply Python coding conventions and type hinting
- Prepare foundation for future enhancements (persistence, web API, testing)

## 🚀 Features

### 📁 Project Management
- **Create Projects** with name (3-30 words) and description (max 150 words)
- **Edit Projects** - modify name and description with validation
- **Delete Projects** with automatic cascade deletion of associated tasks
- **List Projects** - view all projects with IDs and descriptions
- **Unique Naming** - prevent duplicate project names
- **Configurable Limits** - maximum projects controlled via environment variables

### ✅ Task Management
- **Add Tasks** to projects with title, description, status, and optional deadline
- **Change Task Status** - update between `todo`, `doing`, and `done` states
- **Edit Tasks** - modify title, description, and deadline
- **Delete Tasks** - remove individual tasks from projects
- **List Tasks** - view all tasks within a specific project
- **Validation** - ensure valid statuses and future deadlines

### ⚙️ System Features
- **In-Memory Storage** - lightweight data persistence during runtime
- **Environment Configuration** - customizable limits via `.env` file
- **Comprehensive Error Handling** - meaningful error messages and validation
- **Type Safety** - full type hinting throughout the codebase

## 🛠 Installation & Setup

### Prerequisites
- Python 3.12 or higher
- Poetry (dependency management)

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd todolist

# Install dependencies using Poetry
poetry install

# Configure environment (optional)
cp .env.example .env
# Edit .env to adjust limits if needed
```

### Environment Configuration
Create a `.env` file with the following variables:
```env
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS_PER_PROJECT=50
```

## 📖 Usage Guide

### Starting the Application
```bash
poetry run python main.py
```

### Available Commands

#### Project Commands
```bash
create_project "Project Name" "Project Description"
edit_project 1 "Updated Name" "Updated Description"
delete_project 1
list_projects
```

#### Task Commands
```bash
add_task 1 "Task Title" "Task Description" "todo" "2025-10-25"
change_task_status 1 2 "doing"
edit_task 1 2 "New Title" "New Description" "2025-10-26"
delete_task 1 2
list_tasks 1
```

#### System Commands
```bash
help      # Display available commands
exit      # Quit the application
```

### Example Session
```bash
> create_project "Learning Python" "Master Python programming concepts"
✅ Project created successfully:
   ID: 1, Name: Learning Python, Description: Master Python programming concepts

> add_task 1 "Study OOP" "Learn classes, inheritance, and polymorphism" "todo"
✅ Task added successfully:
   ID: 1, Title: Study OOP, Status: todo

> list_tasks 1
📋 Tasks for 'Learning Python':
   1. [todo] Study OOP - Learn classes, inheritance, and polymorphism
```

## 🏗 Project Architecture

### Directory Structure
```
todolist/
├── todolist/
│   ├── application/
│   │   └── services.py     # Business logic services
│   ├── domain/
│   │   └── models.py       # Domain models (Project, Task)
│   ├── infrastructure/
│   │   └── repository.py   # In-memory storage
│   └── config.py           # Environment config
├── main.py                 # CLI entry point
├── pyproject.toml          # Poetry config
├── .env                    # Sample env file
└── .gitignore              # Git ignore
```

## 🔧 Development

### Technology Stack
- **Language**: Python 3.12+
- **Dependency Management**: Poetry
- **Code Quality**: Type hints, PEP8 compliance, comprehensive docstrings
- **Version Control**: Git with conventional commits
