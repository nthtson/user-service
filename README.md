# User Service – E-Commerce Microservice Architecture

## Overview
The User Service is a core microservice in a large-scale, distributed e-commerce platform, responsible for managing all user-related functionalities including registration, authentication, profile management, and user lifecycle operations. Designed for scalability and security, this service integrates tightly with other services (e.g., Orders, Cart, Notification) in a cloud-native, event-driven architecture.

---

## Key Features

- **User Registration & Management**  
  Create and manage user accounts with validation and secure password hashing.

- **JWT-Based Authentication**  
  Stateless authentication using JSON Web Tokens (JWT) for secure session handling.

- **Profile Update & Retrieval**  
  Endpoints for authenticated users to fetch and update personal details.

- **Event-Driven Communication**  
  Publishes user events (e.g., `user_created`, `user_deleted`) via RabbitMQ for downstream services.

- **API Versioning**  
  Supports clean API versioning (`/api/v1/...`) for smooth iteration and backward compatibility.

- **Production-Ready Stack**  
  Built with scalability, observability, and resilience as primary concerns.
---
## Tech Stack

| Category                  | Technology                                    |
|---------------------------|-----------------------------------------------|
| Language                  | Python 3.12                                   |
| Framework                 | Flask (with MethodView for class-based views) |
| Database                  | PostgreSQL (via SQLAlchemy ORM)               |
| Messaging                 | RabbitMQ (event-based communication)          |
| Auth                      | JWT (token issuance and verification)         |
| Containerization          | Docker, Docker Compose                        |
| Orchestration             | Kubernetes (K8s)                              |
| Infra-as-Code             | Terraform                                     |
| CI/CD                     | GitHub Actions                                |
| Code Quality              | `black`, `isort`, `flake8`, `pylint`, `mypy`  |
| Error Monitoring          | Sentry                             |
| APM + Performance Insights | New Relic                                              |
| SMTP service              | Mailtrap                                            |

---
## Scalability & Extensibility

- **Scalable** for multi-tenant architectures using Kubernetes
- **Modular** for easy integration of external auth providers (e.g., Google OAuth)
- **Event-Ready** for triggering workflows like welcome emails or verification flows

---

## Project Structure

```markdown
user_service/
├── app/
│   ├── __init__.py
│   ├── core/                   # Auth, JWT, middlewares, utils
│   ├── db/                     # SQLAlchemy init, session, migrations
│   ├── extensions/             # Shared extensions like Sentry initialization
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── api/                # Blueprints
│   │   ├── models/             # SQLAlchemy models
│   │   ├── views/              # Flask class-based views (routes)
│   │   ├── services/           # Business logic
│   │   ├── repositories/       # DB queries
│   │   ├── schemas/            # Pydantic or Marshmallow schemas
│   │   └── events/             # RabbitMQ producers/publishers
├── tests/                      # Unit/integration tests
│   ├── v1/
│   ├── conftest.py
├── migrations/                 # Alembic migrations
├── Dockerfile                  # Docker image definition (build instructions) for api
├── Dockerfile.worker           # Docker image definition (build instructions) for worker
├── docker-compose.yml          # Optional: multi-container setup (e.g. with DB)
├── requirements.txt            # Python dependencies
├── config.py                   # App configurations
├── wsgi.py                     # Gunicorn entrypoint
├── .env                        # Local environment config
├── .flake8                     # Flake8 config (style & lint rules) → Controls line length, ignores, excludes, etc.
├── .pylintrc                   # Pylint config (code quality and linting) → Static analysis tool for finding bugs & smells
├── .isort.cfg                  # Isort config (import sorting) → Keeps imports clean and consistent
├── mypy.ini                    # Mypy config (type checking) → Enforces and checks type annotations
├── email_worker.py             # Background worker that listens to RabbitMQ and sends emails
├── README.md
└── .github
    └── workflows
        └── ci.yml              # Github Action (CI/CD)
```