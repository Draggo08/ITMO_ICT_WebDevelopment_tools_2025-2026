# Lab 1 (15 points)

FastAPI project with PostgreSQL, SQLAlchemy ORM, Alembic migrations, JWT auth, and password hashing.

## What is implemented

- 6 tables (`users`, `projects`, `skills`, `project_memberships`, `tasks`, `comments`)
- One-to-many relations:
  - `projects -> tasks`
  - `tasks -> comments`
  - `users -> comments`
- Many-to-many relation:
  - `users <-> projects` through `project_memberships`
  - Associative table has extra fields: `role`, `joined_at`, `skill_id`
- CRUD-style API endpoints for major entities
- User functionality for 15-point requirement:
  - registration
  - login
  - JWT token generation
  - JWT authentication
  - password hashing
  - extra methods: current user, user list, password change

## Start

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and set values.
4. Run migrations:

```bash
alembic upgrade head
```

5. Start app:

```bash
uvicorn app.main:app --reload
```

## API routes

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/users/me`
- `GET /api/users`
- `POST /api/users/change-password`
- `POST /api/skills`
- `GET /api/skills`
- `POST /api/projects`
- `GET /api/projects`
- `POST /api/projects/{project_id}/memberships`
- `GET /api/projects/{project_id}/memberships`
- `POST /api/projects/{project_id}/tasks`
- `GET /api/projects/{project_id}/tasks`
- `POST /api/tasks/{task_id}/comments`
- `GET /api/tasks/{task_id}/comments`
