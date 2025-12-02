# To Do List Project – Phase 3 (Web API)  

![Phase 3](https://img.shields.io/badge/Phase-3%20Web%20API-100%25%20Complete-success)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791?logo=postgresql)

**Software Engineering Course – AUT – November 2025**

---

## DEPRECATION NOTICE – CLI IS OFFICIALLY DEPRECATED

> **The old Command-Line Interface (CLI) from Phase 1 & 2 is deprecated as of Phase 3.**  
> It still works for backward compatibility, but it displays a clear warning on startup and will be removed in future versions.  
> **All new development and usage must go through the new Web API.**

**Please use the Web API instead:**  
http://localhost:8000/docs (Swagger UI)  
http://localhost:8000/redoc (ReDoc)

---

## Project Evolution Summary

| Phase | Year | Storage           | Architecture                  | Interface                 | Status       |
|------|------|-------------------|-------------------------------|---------------------------|--------------|
| 1    | 2024 | In-Memory         | OOP + Basic Structure         | CLI                       | Completed    |
| 2    | 2025 | PostgreSQL + SQLAlchemy | Full Layered Architecture + Repository Pattern + Scheduler | CLI + Persistent DB | Completed    |
| **3**    | **2025** | **PostgreSQL**        | **Layered + Presentation Layer** | **RESTful Web API (FastAPI)** | **Current** |

**Phase 3 introduces a complete, production-ready Web API** while preserving 100% of the existing domain logic, services, and repositories from Phase 2.

---

## Features – Phase 3 Web API

- Full RESTful API with proper resource naming (`/tasks`, not verbs)
- Built with **FastAPI** – automatic OpenAPI (Swagger) & ReDoc documentation
- Professional input validation using **Pydantic**
- Pagination, filtering, and full-text search (`?skip=`, `?limit=`, `?completed=`, `?q=`)
- Nested category support (`category` object returned with each task)
- Proper HTTP status codes (201 Created, 204 No Content, etc.)
- Eager loading of relationships (Task + Category)
- Complete statistics endpoint (`GET /tasks/stats`)
- Ready for Frontend (React, Vue, etc.) or Mobile App integration
- CORS-ready (add middleware if needed)
- Clean layered architecture preserved:
  ```
  Presentation (API) → Service → Repository → Domain → Database
  ```

---

## API Documentation (Auto-generated)

After starting the server:

- **Interactive Swagger UI**: http://localhost:8000/docs
- **Beautiful ReDoc**: http://localhost:8000/redoc

All endpoints, request/response models, and examples are documented automatically.

### Main Endpoints

| Method | Endpoint                    | Description                       |
|--------|-----------------------------|-----------------------------------|
| GET    | `/tasks`                    | List tasks (with pagination & filters) |
| GET    | `/tasks/{id}`               | Get single task                   |
| POST   | `/tasks`                    | Create new task                   |
| PATCH  | `/tasks/{id}`               | Partial update                    |
| PATCH  | `/tasks/{id}/complete`      | Mark as completed                 |
| DELETE | `/tasks/{id}`               | Delete task                       |
| GET    | `/tasks/stats`              | Task statistics                   |

---

## How to Run (Phase 3 – Recommended)

```bash
# 1. Install dependencies
poetry install

# 2. Start PostgreSQL (make sure it's running and DATABASE_URL is set)

# 3. Run the Web API (recommended)
uvicorn todolist.main:app --reload --port 8000
```

Then open: http://localhost:8000/docs

---

## Running the Old CLI (Deprecated – Shows Warning)

```bash
python -m todolist.main_cli
```

You will see:

```
WARNING: CLI interface is officially DEPRECATED (Phase 3).
Please migrate to the new Web API at http://localhost:8000/docs
CLI will be removed in a future version.
```

---

## Project Structure (Phase 3)

```
src/todolist/
├── api/                  # New Presentation Layer (Phase 3)
│   ├── routers/
│   ├── schemas.py
│   └── dependencies.py
├── domain/               # Unchanged from Phase 2
├── repositories/         # Minor enhancements only (pagination + eager load)
├── services/             # Enhanced for API use (no logic change)
├── db/                   # Database session & models
├── cli/                  # Deprecated but still functional
├── scheduler/            # Still works independently
└── main.py               # FastAPI entry point
```

---

## Technology Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0+
- **Database**: PostgreSQL
- **Validation & Docs**: Pydantic + OpenAPI
- **Package Manager**: Poetry
- **Development Server**: Uvicorn