# 🔐 Auth API

Auth API is a backend authentication service built with FastAPI, PostgreSQL, and SQLAlchemy.  
It implements secure JWT-based authentication with refresh token rotation and multi-device session control.

The project focuses on production-style authentication patterns, including token revocation, session limits, and secure refresh flows.

---

## 🚀 Key Features

- User registration with email and password
- JWT access tokens (short-lived)
- Refresh token system with rotation
- Limit of 5 active refresh tokens per user
- Logout from single device (token revocation)
- Logout from all devices (global session invalidation)
- Secure authentication via Bearer tokens
- Refresh token hashing and validation
- Suspicious refresh detection (invalidates all sessions)

---

## 🧠 Domain Model Overview
```text
User
└── RefreshToken
```
### Core relationships

- **User → RefreshToken**
  - Each user can have multiple active refresh tokens
  - Maximum of 5 active tokens per user
  - Tokens are stored and validated server-side

## 🧱 Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy ORM
- PostgreSQL 17
- Alembic
- JWT (python-jose)
- passlib / pwdlib
- python-dotenv
- uvicorn

## 🔐 Authentication Design

- Access tokens expire after 15 minutes
- Refresh tokens expire after 7 days
- Refresh tokens are hashed before storage
- Rotation: every refresh issues a new pair of tokens
- Device/session tracking via refresh tokens
- Security mechanism detects suspicious refresh attempts and invalidates all sessions

## 📡 API Overview

### Auth
- POST `/auth/register` — Register user
- POST `/auth/login` — Login user (returns access + refresh tokens)
- POST `/auth/refresh` — Refresh tokens
- POST `/auth/logout` — Revoke single session
- POST `/auth/logout_all` — Revoke all sessions

### Users
- GET `/users/me` — Get current authenticated user

## ⚙️ Setup & Run
### 1. Create and activate the virtual environment
```bash
source env/bin/activate
```

### 2. Start PostgreSQL (Docker)
```bash
docker-compose up -d
```

### 3. Environment variables
Create a `.env` file or export variables:
```env
SECRET_KEY=YourJWTSecretKey
ALGORITHM=HS256
```

### 4. Run migrations
```bash
alembic upgrade head
```

### 5. Run application
```bash
uvicorn main:app --reload
```

App URLs:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## 🧩 Architecture Notes
- Short-lived access tokens + long-lived refresh tokens
- Stateless authentication with server-side session control
- Secure refresh rotation system
- Database-backed token revocation system

## 🧠 What This Project Demonstrates
- Production-grade authentication design
- JWT + refresh token architecture
- Session management across multiple devices
- Secure token storage strategies
- Backend security best practices in FastAPI