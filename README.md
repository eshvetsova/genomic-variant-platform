# Genomic Variant Analysis Platform

A FastAPI REST API for uploading, filtering, annotating, and summarizing VCF files, backed by PostgreSQL and AWS S3.

## Tech stack

- FastAPI and Python 3.15+
- Poetry
- PostgreSQL (AWS RDS or Docker Compose)
- AWS S3
- AWS ECS Fargate

## Local development

Prerequisites: Python 3.15+, Poetry, and Docker Compose.

```bash
poetry install --with dev
cp .env.example .env
docker compose up --build
```

The Compose stack starts PostgreSQL, applies pending SQL migrations, then starts the API. The API listens on `http://localhost:8000`. The separate test database listens on `127.0.0.1:5433`; the application database listens on `127.0.0.1:5432`.

Configure local credentials and service values in `.env`; do not commit that file. The checked-in Compose credentials are for local development only.

### Tests

Start the isolated test database and run the complete suite, including PostgreSQL integration tests:

```bash
docker compose up -d db-test
TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/variants_test poetry run pytest
```

## API routes

Project routes are versioned under `/api/v1`:

- `POST /api/v1/projects/` — create a project
- `GET /api/v1/projects/` — list projects, oldest first
- `DELETE /api/v1/projects/{project_id}/` — delete a project by its UUID

`GET /health` is unversioned and is used by the container health check.

OpenAPI documentation is available at `/api/v1/openapi.json`.

Migrations are applied by the one-off `migrate` Compose service before the API starts. Migration `0002` converts existing integer project IDs to UUIDs, assigning new IDs to existing rows.
