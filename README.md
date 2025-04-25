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
├── infra/                      # Terraform infrastructure modules (EKS, RDS, AWS MQ, ACM, Route53, IAM)
├── herm-chart/                 # Helm chart with configurable values and Kubernetes manifests
└── .github
    └── workflows
        ├── ci.yml              # Github Actions: handles lint, test, type check
        └── deploy.yml          # Github Actions: handles Docker build/push + EKS/Helm deploy
```
---

## User Service Deployment

### Overview

- 📦 Terraform infrastructure modules (EKS, RDS, AWS MQ, ACM, Route53, IAM)
- 📁 Helm chart with configurable values and Kubernetes manifests
- ⚙️ GitHub Actions pipeline for CI/CD

## Infrastructure Plan: User Service (AWS Free Tier Optimized)

### Overview
This infrastructure plan sets up a scalable, cost-effective backend for the User microservice, using AWS services and Kubernetes (EKS), while optimizing for the AWS Free Tier.

---

### Core Infrastructure (Provisioned via Terraform)

| Component         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **VPC**          | Custom or default VPC to isolate networking resources                        |
| **Subnets**      | 2 public subnets (for EKS + NAT), or reused from default VPC                |
| **EKS Cluster**  | 1-node `t3.micro` (free tier), hosting Flask app & email worker             |
| **RDS**          | PostgreSQL `db.t3.micro`, 20GB storage (free tier)                          |
| **RabbitMQ**     | Local (Docker-based), not AWS MQ (to avoid cost)                            |
| **NodePort SVC** | Exposes the app using port `30080`, no ALB used                            |
| **Security Groups** | Minimal SGs: EKS -> RDS (port 5432)                                    |

---

### Deployables

| Component         | Runtime        | Deployed As      | Scaling   |
|------------------|----------------|------------------|-----------|
| Flask API        | Python + Gunicorn | Helm Deployment | Manual (replica=1) |
| Email Worker     | Python script  | Helm Deployment  | Manual (replica=1) |
| PostgreSQL       | AWS RDS        | Provisioned      | Managed   |
| RabbitMQ         | Docker service | Compose only     | Local     |

---

### Access & Routing

- App URL: `http://<eks-node-ip>:30080`
- DNS mapping to `api.example.site` is **manual** (via A record)
- SSL: Optional (not deployed)

---

### Infrastructure Modules

| Module        | Files                                               |
|---------------|-----------------------------------------------------|
| EKS           | `eks/eks-cluster.tf`, IAM roles, node group         |
| RDS           | `rds/rds-postgres.tf`, security group for RDS       |
| IAM           | `iam/roles.tf` for EKS & worker pods                |
| Helm Chart    | `helm-chart/` for app + worker deployments          |
| GitHub Actions| `.github/workflows/deploy.yml`                     |

---

### Optional Enhancements (Later)

- Add NGINX Ingress + SSL
- Use cert-manager + Let's Encrypt
- External Secrets Operator
- Autoscaling (HPA) for pods
- Logging to CloudWatch or Loki
- Monitoring via Prometheus + Grafana

---