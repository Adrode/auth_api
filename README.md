# Auth API

Authentication service built with FastAPI, PostgreSQL, and SQLAlchemy. Uses JWT access tokens and refresh tokens.

## What this project does

- Registers users with email/password
- Issues JWT access tokens
- Handles refresh tokens with a limit of 5 active refresh tokens per user
- Supports logging out a single refresh token and logging out from all devices
- Provides protected endpoints secured with Bearer JWT

## Architecture

- `main.py` - FastAPI application entry point
- `api/auth.py` - endpoints for registration, login, token refresh, and logout
- `api/users.py` - endpoint for the currently authenticated user
- `database/models.py` - SQLAlchemy models: `User` and `RefreshToken`
- `database/database.py` - PostgreSQL connection setup and database initialization
- `authentication/short.py` - JWT handling and authentication helper functions
- `authentication/long.py` - refresh token generation and hashing
- `schemas/schemas.py` - Pydantic models for request and response schemas

## Requirements

- Python 3.12
- PostgreSQL 17 (can be run locally or with `docker-compose`)
- Python dependencies:
  - `fastapi`
  - `uvicorn`
  - `sqlalchemy`
  - `psycopg2-binary`
  - `python-dotenv`
  - `python-jose`
  - `pwdlib`
  - `passlib`
  - `email-validator`

## Environment setup

1. Activate the virtual environment:

```bash
source env/bin/activate
```

2. Install dependencies (if not installed yet):

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-jose pwdlib passlib email-validator
```

3. Create a `.env` file in the project root with the following values:

```env
SECRET_KEY=YourJWTSecretKey
ALGORITHM=HS256
```

> The database connection is currently configured directly in `database/database.py` as:
> `postgresql+psycopg2://auth_api_user:auth_api_passwd@localhost:5432/auth_api_db`

## Running the database

Use `docker-compose` to start PostgreSQL:

```bash
docker-compose up -d
```

Docker Compose settings from `docker-compose.yml`:

- user: `auth_api_user`
- password: `auth_api_passwd`
- database: `auth_api_db`
- port: `5432`

## Running the application

```bash
uvicorn main:app --reload
```

The application will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Endpoints

### Register

`POST /auth/register`

Request body:

```json
{
  "email": "user@example.com",
  "password": "SuperSecretPassword"
}
```

### Login

`POST /auth/login`

Form data (`application/x-www-form-urlencoded`):

- `username` - user email
- `password` - password

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "refresh_token": "..."
}
```

### Refresh token

`POST /auth/refresh`

Request body:

```json
{
  "refresh_token": "..."
}
```

Response returns a new `access_token` and a new `refresh_token`.

### Logout single token

`POST /auth/logout`

Request body:

```json
{
  "refresh_token": "..."
}
```

### Logout from all devices

`POST /auth/logout_all`

Request body:

```json
{
  "refresh_token": "..."
}
```

### Get current user

`GET /users/me`

Header:

```http
Authorization: Bearer <access_token>
```

## Notes

- The active refresh token limit per user is `5`. When the limit is exceeded, the oldest token is removed.
- Refresh token renewal validates `user-agent`; suspicious refresh attempts remove all tokens and return an error.
- Access tokens expire after `15` minutes, refresh tokens expire after `7` days.

## Extensions

The project includes `auth_api_migrations` with Alembic configuration, which can be used later to manage database migrations.

---

## Contact

If you want, I can also add a section with sample `curl` commands, database schema details, or Docker-based startup automation.
