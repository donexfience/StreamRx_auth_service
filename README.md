# Auth Service

This project implements a clean architecture for an authentication service using FastAPI, PostgreSQL, and GraphQL. It provides user registration, login, and authentication with JWT token generation and validation.

## Features

- **Clean Architecture:**
  - Separation of concerns into layers: **Presentation**, **Domain**, **Application**, and **Infrastructure**.
  - Loose coupling for scalability and flexibility.
  
- **GraphQL API:**
  - User registration, login, and authentication.
  - Secure JWT-based token generation and validation.
  
- **Database:**
  - PostgreSQL integration with SQLAlchemy and async support.

- **Asynchronous Execution:**
  - Fully async for high performance using FastAPI.

## Tech Stack

- **Framework**: FastAPI
- **GraphQL**: Strawberry GraphQL
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT via `python-jose` and `passlib`
- **Environment Management**: `Pydantic` and `python-dotenv`

## Requirements

- Python 3.10+
- PostgreSQL
- Pipenv or pip for dependency management

---

## Clean Architecture Layers

1. **Presentation Layer**:
   - Handles the user-facing API.
   - FastAPI and GraphQL endpoints.

2. **Domain Layer**:
   - Core business logic.
   - Pure Python entities (e.g., `User`, `AuthToken`).
   - No external dependencies.

3. **Application Layer**:
   - Coordinates use cases such as user registration and login.
   - Encapsulates the business logic and interacts with the domain layer.

4. **Infrastructure Layer**:
   - Handles external concerns such as:
     - Database (PostgreSQL via SQLAlchemy).
     - JWT handling.
     - Password hashing with `passlib`.

---

## Project Structure

```plaintext
auth-service/
├── app/
│   ├── presentation/          # FastAPI and GraphQL routes
│   │   ├── graphql/           # Strawberry GraphQL schemas
│   │   ├── api/               # REST API routes (if any)
│   │   └── main.py            # FastAPI entry point
│   ├── domain/                # Core business logic
│   │   ├── entities/          # Domain entities (e.g., User, Token)
│   │   └── exceptions.py      # Custom domain exceptions
│   ├── application/           # Use cases
│   │   ├── services/          # Core service logic (e.g., AuthService)
│   │   └── interfaces/        # Interfaces for repositories
│   ├── infrastructure/        # External dependencies
│   │   ├── database/          # Database models and repositories
│   │   ├── auth/              # JWT and password hashing utilities
│   │   └── config.py          # Configuration management
│   └── tests/                 # Unit and integration tests
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
└── alembic/                   # Database migrations (if using Alembic)
