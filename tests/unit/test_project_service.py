import logging
from uuid import UUID

import pytest

from app.domain.errors import ProjectNotFoundError
from app.infrastructure.memory.projects import InMemoryProjectRepository
from app.services.projects import ProjectService


@pytest.mark.anyio
async def test_service_strips_input_and_logs_created_id(caplog, anyio_backend):
    caplog.set_level(logging.INFO, logger="app.services.projects")
    service = ProjectService(InMemoryProjectRepository())

    project = await service.create_project("  Cohort  ", " Dr. Ada ")

    assert project.name == "Cohort"
    assert project.lead_scientist == "Dr. Ada"
    assert isinstance(project.project_id, UUID)
    assert f"project_id={project.project_id}" in caplog.text


@pytest.mark.anyio
async def test_service_lists_and_deletes_project(anyio_backend):
    service = ProjectService(InMemoryProjectRepository())
    project = await service.create_project("Cohort", "Dr. Ada")

    assert [item.project_id for item in await service.list_projects()] == [project.project_id]
    await service.delete_project(project.project_id)
    assert await service.list_projects() == []


@pytest.mark.anyio
async def test_service_raises_domain_error_for_missing_project(anyio_backend):
    service = ProjectService(InMemoryProjectRepository())

    with pytest.raises(ProjectNotFoundError):
        await service.delete_project(UUID(int=1))
