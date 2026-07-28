# Task Tracker Lite

User authentication, roles & task management with categories.
FastAPI + PostgreSQL + SQLAlchemy, fully Dockerized.

**Demo video:**

## Quick start

```bash
cp .env.example .env      # edit SECRET_KEY at minimum
docker compose up --build
```

API runs at http://localhost:8000 — interactive docs at http://localhost:8000/docs

A default admin is seeded on startup using `ADMIN_EMAIL` / `ADMIN_PASSWORD` from `.env`.

## Architecture (MVC)

- **Models** (`app/models/`) — SQLAlchemy tables: User (with role), Category, Task
- **Views** — API-only project, so the "view" layer is the JSON response schemas in `app/schemas/`
- **Controllers** (`app/controllers/`) — thin FastAPI routers that delegate to `app/services/` where business logic lives

## API overview

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | /auth/register | Public | Register (name, email, password, confirm_password) |
| POST | /auth/login | Public | Login, returns JWT |
| POST | /auth/logout | Authenticated | Invalidates current token |
| GET | /auth/me | Authenticated | Current user info |
| GET | /categories | Authenticated | List categories |
| POST | /categories | **Admin** | Create category |
| PUT | /categories/{id} | **Admin** | Update category |
| DELETE | /categories/{id} | **Admin** | Delete category |
| GET | /tasks | Authenticated | List own tasks |
| POST | /tasks | Authenticated | Create task (title, description, status, due_date, category_id) |
| PUT | /tasks/{id} | Authenticated | Update own task |
| DELETE | /tasks/{id} | Authenticated | Delete own task |
| GET | /admin/tasks | **Admin** | Dashboard: all tasks, filter by `user_id`, `status`, `due_before`, `due_after` |

## Business rules

- Passwords stored bcrypt-hashed; emails unique
- All routes except register/login require a valid Bearer token
- Normal users cannot create/update/delete categories (403)
- **Status of a task cannot be changed after its due date has passed** (400)

## Auth flow

Send the token from `/auth/login` as a header:

```
Authorization: Bearer <token>
```

Logout adds the token to a blacklist. This is in-memory for simplicity — in production it would be Redis with TTL, or short-lived access tokens + refresh tokens.
