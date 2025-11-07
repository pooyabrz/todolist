# ToDoList - Phase 2 (Database Integration)

A task management application (ToDoList) with persistent storage in PostgreSQL.

## 🎯 Phase 2 Features

- ✅ Persistent storage in PostgreSQL
- ✅ SQLAlchemy ORM usage
- ✅ Migration management with Alembic
- ✅ Layered Architecture (Repository Pattern)
- ✅ Automatic overdue task closure with Scheduler
- ✅ Docker support for database

## 📋 Prerequisites

- Python 3.10+
- Docker Desktop
- Poetry (package manager)

## 🚀 Installation & Setup

### 1. Clone the Project
```bash
git clone <repository-url>
cd todolist
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Set Up Database with Docker
```bash
# Create .env file from template
cp .env.example .env

# Edit .env and configure database information
# Then run Docker:
docker-compose up -d

# Check status
docker ps
```

### 4. Run Migrations
```bash
# Apply migrations
poetry run alembic upgrade head

# Check database connection
poetry run python main.py db:check
```

## 📖 Usage

### Main Commands

```bash
# View help
poetry run python main.py help

# List tasks
poetry run python main.py tasks:list

# Create new task
poetry run python main.py tasks:create

# Complete task
poetry run python main.py tasks:complete 1

# Task statistics
poetry run python main.py tasks:stats
```

### Scheduler (Automatic Overdue Task Closure)

```bash
# Run once
poetry run python main.py tasks:autoclose-overdue

# Run in daemon mode (every 15 minutes)
poetry run python main.py tasks:autoclose-overdue --daemon
```

## 🏗️ Project Structure

```
todolist/
├── src\todolist/
│   ├── domain/          # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   ├── services/         # Business logic
│   ├── cli/             # User interface
│   ├── scheduler/       # Scheduled tasks
│   └── db/              # Database configuration
├── alembic/             # Migration files
├── docker-compose.yml   # Docker configuration
├── pyproject.toml       # Dependencies
└── main.py              # Entry point
```

## 🔄 Migration Workflow

```bash
# Create new migration after model changes
poetry run alembic revision --autogenerate -m "description"

# Apply migration
poetry run alembic upgrade head

# Revert to previous version
poetry run alembic downgrade -1

# View history
poetry run alembic history
```

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check Docker status
docker ps

# View PostgreSQL logs
docker logs todolist-db

# Restart database
docker-compose restart
```

### Reset and Start Over

```bash
# Remove database and volumes
docker-compose down -v

# Restart
docker-compose up -d
poetry run alembic upgrade head
```

## 📚 Key Concepts

### Repository Pattern
Separation of data access logic from business logic

### ORM (Object-Relational Mapping)
Converting Python objects to database records

### Migration
Version control and management of database schema changes

### Scheduler
Automated execution of tasks at specified times