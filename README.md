# SIEM Lab (MVP)

Mini SIEM educativo (DAM / Blue Team): ingesta de eventos, motor de reglas y gestión de alertas.

## Stack
- FastAPI + Uvicorn
- PostgreSQL
- SQLAlchemy + Alembic
- Docker Compose
- Tests: pytest

## Run (Docker)
```bash
docker compose -f docker/compose.yml up -d --build
```

## URLs

API docs: http://127.0.0.1:8000/docs

Adminer: http://127.0.0.1:8080

## Key endpoints

POST /ingest

GET /alerts

GET /alerts/ui

GET /health
