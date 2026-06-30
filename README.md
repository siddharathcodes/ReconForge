# ReconForge

Production-grade cybersecurity reconnaissance platform.

## Stack

- Python 3.12, FastAPI, SQLAlchemy 2, Alembic
- PostgreSQL, Redis, Celery
- React 19, TypeScript, Vite, TailwindCSS
- Docker Compose

## Local Development

```bash
docker compose up --build
```

Backend: `http://localhost:8000`

Frontend: `http://localhost:8080`

Health: `http://localhost:8000/api/v1/health`
