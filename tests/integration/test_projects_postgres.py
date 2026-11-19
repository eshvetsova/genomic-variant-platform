import pytest

from app.db.migrate import apply_migrations


@pytest.mark.integration
@pytest.mark.anyio
async def test_database_migrations_apply_in_a_rolled_back_transaction(
    postgres_engine, anyio_backend
):
    async with postgres_engine.connect() as connection:
        transaction = await connection.begin()
        try:
            await apply_migrations(connection)
        finally:
            await transaction.rollback()


@pytest.mark.integration
@pytest.mark.anyio
async def test_project_crud_persists_in_postgres_and_rolls_back(postgres_client):
    created = await postgres_client.post(
        "/api/v1/projects/",
        json={
            "name": "Postgres integration cohort",
            "lead_scientist": "Dr. Postgres",
            "description": "Uses the real database driver and SQL",
        },
    )
    assert created.status_code == 201
    project_id = created.json()["project_id"]

    listed = await postgres_client.get("/api/v1/projects/")
    assert [row["project_id"] for row in listed.json()] == [project_id]

    deleted = await postgres_client.delete(f"/api/v1/projects/{project_id}/")
    assert deleted.status_code == 204
    assert (await postgres_client.get("/api/v1/projects/")).json() == []


@pytest.mark.integration
@pytest.mark.anyio
async def test_postgres_duplicate_name_returns_conflict(postgres_client):
    payload = {"name": "Duplicate in PostgreSQL", "lead_scientist": "Dr. DB"}
    assert (await postgres_client.post("/api/v1/projects/", json=payload)).status_code == 201

    duplicate = await postgres_client.post("/api/v1/projects/", json=payload)
    assert duplicate.status_code == 409


@pytest.mark.integration
@pytest.mark.anyio
async def test_postgres_delete_missing_project_returns_not_found(postgres_client):
    response = await postgres_client.delete(
        "/api/v1/projects/00000000-0000-0000-0000-000000000001/"
    )
    assert response.status_code == 404
