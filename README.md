# Task Tracker Lite

A role-based Task Management REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The application implements secure JWT authentication, role-based authorization, category management, task management, and an admin dashboard with filtering capabilities. The entire application is fully Dockerized for easy deployment.

## Features

- JWT-based Authentication (Register, Login, Logout)
- Secure password hashing using **bcrypt**
- Role-based Authorization (**Admin** & **Normal User**)
- Category Management (Admin only)
- Task Management with Categories
- User-specific task ownership
- Admin Dashboard with task filtering
- Dockerized backend and PostgreSQL
- Interactive Swagger API Documentation
- MVC-based project structure

---

## Tech Stack

- **Backend:** FastAPI
- **Language:** Python 3.12
- **Database:** PostgreSQL 16
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Passlib (bcrypt)
- **Containerization:** Docker & Docker Compose

---

# Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/task-tracker-lite.git
cd task-tracker-lite
```

## 2. Configure environment variables

```bash
cp .env.example .env
```

Update the values inside `.env` if required (especially `SECRET_KEY`).

## 3. Start the application

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

Interactive Swagger Documentation:

```
http://localhost:8000/docs
```

---

## Default Admin User

A default administrator account is automatically seeded during application startup using the following environment variables:

```
ADMIN_EMAIL
ADMIN_PASSWORD
```

These values can be configured in the `.env` file.

---

# Project Structure

```
app/
│
├── controllers/      # FastAPI route handlers
├── core/             # Authentication & dependencies
├── models/           # SQLAlchemy models
├── schemas/          # Request/Response schemas
├── services/         # Business logic
├── database.py
├── config.py
└── main.py
```

---

# Architecture (MVC)

- **Models** (`app/models/`)  
  SQLAlchemy models representing Users, Categories and Tasks.

- **Views** (`app/schemas/`)  
  JSON request and response schemas returned by the API.

- **Controllers** (`app/controllers/`)  
  FastAPI routers responsible for handling HTTP requests and delegating business logic to the service layer.

- **Services** (`app/services/`)  
  Implements the application's business rules and database interactions.

---

# API Overview

| Method | Endpoint | Access | Description |
|----------|----------------------|--------------|-------------------------------------------|
| POST | `/auth/register` | Public | Register a new user |
| POST | `/auth/login` | Public | Login and receive JWT token |
| POST | `/auth/logout` | Authenticated | Logout and invalidate current token |
| GET | `/auth/me` | Authenticated | Get current user |
| GET | `/categories` | Authenticated | List all categories |
| POST | `/categories` | **Admin** | Create category |
| PUT | `/categories/{id}` | **Admin** | Update category |
| DELETE | `/categories/{id}` | **Admin** | Delete category |
| GET | `/tasks` | Authenticated | View own tasks |
| POST | `/tasks` | Authenticated | Create a task |
| PUT | `/tasks/{id}` | Authenticated | Update own task |
| DELETE | `/tasks/{id}` | Authenticated | Delete own task |
| GET | `/admin/tasks` | **Admin** | View all tasks with filters |

---

# Authentication

After logging in, include the returned JWT token in every protected request.

```
Authorization: Bearer <token>
```

---

# Business Rules

- Passwords are securely hashed using **bcrypt**.
- Email addresses must be unique.
- All APIs except **Register** and **Login** require authentication.
- Only **Admin** users can create, update or delete categories.
- Normal users can only assign tasks to existing categories.
- Users can only view and modify **their own tasks**.
- Task status cannot be modified **after the due date has passed**.
- The Admin dashboard allows filtering by:
  - User
  - Status
  - Due Before
  - Due After

---

# Logout Implementation

Logout is implemented using an **in-memory JWT blacklist**.

When a user logs out, the current token is added to a blacklist and any subsequent requests using that token are rejected with **401 Unauthorized**.

This implementation is appropriate for the assessment's single-process deployment.

In a production environment, token revocation would typically be implemented using a shared persistent store such as **Redis** or **PostgreSQL**, or by using short-lived access tokens together with refresh tokens.

---

# Environment Variables

Configuration is managed through `.env`.

Example variables:

```
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES

ADMIN_EMAIL
ADMIN_PASSWORD
```

Refer to `.env.example` for the complete configuration.

---

# Assumptions

- All newly registered users are created as **Normal Users**.
- Administrator accounts are seeded automatically at startup.
- Task status can be updated on the due date but not afterwards.
- The logout blacklist is intentionally kept in memory for this assessment.

---

# License

This project was developed as part of a technical assessment for **Sharp & Tannan Associates**.
