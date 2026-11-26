from uuid import UUID

import pytest


@pytest.mark.anyio
async def test_health_endpoint(api_client):
    response = await api_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.anyio
async def test_request_log_omits_query_string(api_client, caplog):
    import logging

    caplog.set_level(logging.INFO, logger="app.requests")
    response = await api_client.get("/health?token=do-not-log")
    assert response.status_code == 200

    request_logs = [
        record.getMessage() for record in caplog.records if record.name == "app.requests"
    ]
    assert len(request_logs) == 1
    assert "GET" in request_logs[0]
    assert "/health" in request_logs[0]
    assert "do-not-log" not in request_logs[0]


@pytest.mark.anyio
async def test_create_and_list_projects(api_client):
    created = await api_client.post(
        "/api/v1/projects/",
        json={"name": "Cohort A", "lead_scientist": "Dr. Lin", "description": "Pilot"},
    )
    assert created.status_code == 201
    UUID(created.json()["project_id"])
    assert created.json()["name"] == "Cohort A"

    listed = await api_client.get("/api/v1/projects/")
    assert listed.status_code == 200
    assert [project["name"] for project in listed.json()] == ["Cohort A"]

    second = await api_client.post(
        "/api/v1/projects/", json={"name": "Cohort B", "lead_scientist": "Dr. Kim"}
    )
    assert second.status_code == 201
    listed = await api_client.get("/api/v1/projects/")
    assert [project["name"] for project in listed.json()] == ["Cohort A", "Cohort B"]


@pytest.mark.anyio
async def test_create_rejects_invalid_project(api_client):
    response = await api_client.post("/api/v1/projects/", json={"name": "", "lead_scientist": ""})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_rejects_server_owned_fields(api_client):
    response = await api_client.post(
        "/api/v1/projects/",
        json={
            "name": "Client attempt",
            "lead_scientist": "Dr. Ada",
            "project_id": 999,
            "created_at": "2026-01-01T00:00:00Z",
            "completed_at": "2026-01-02T00:00:00Z",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_rejects_duplicate_project_name(api_client):
    payload = {"name": "Repeated cohort", "lead_scientist": "Dr. Ada"}
    assert (await api_client.post("/api/v1/projects/", json=payload)).status_code == 201

    duplicate = await api_client.post("/api/v1/projects/", json=payload)
    assert duplicate.status_code == 409


@pytest.mark.anyio
async def test_delete_project_and_missing_project(api_client):
    created = await api_client.post(
        "/api/v1/projects/", json={"name": "Cohort B", "lead_scientist": "Dr. Chen"}
    )
    project_id = created.json()["project_id"]

    deleted = await api_client.delete(f"/api/v1/projects/{project_id}/")
    assert deleted.status_code == 204
    assert (await api_client.get("/api/v1/projects/")).json() == []

    missing = await api_client.delete(f"/api/v1/projects/{project_id}/")
    assert missing.status_code == 404


@pytest.mark.anyio
async def test_delete_rejects_non_integer_id(api_client):
    response = await api_client.delete("/api/v1/projects/not-a-uuid/")
    assert response.status_code == 422
