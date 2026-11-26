import pytest

from app.domain.errors import ProjectNameAlreadyExistsError
from app.domain.projects import NewProject
from app.infrastructure.memory.projects import InMemoryProjectRepository


@pytest.mark.anyio
async def test_memory_repository_creates_and_lists_projects_in_order(anyio_backend):
    repository = InMemoryProjectRepository()
    first = await repository.create(NewProject("First", "Dr. One"))
    second = await repository.create(NewProject("Second", "Dr. Two"))

    projects = await repository.list()
    assert [project.project_id for project in projects] == [first.project_id, second.project_id]


@pytest.mark.anyio
async def test_memory_repository_rejects_duplicate_names(anyio_backend):
    repository = InMemoryProjectRepository()
    await repository.create(NewProject("Unique", "Dr. One"))

    with pytest.raises(ProjectNameAlreadyExistsError):
        await repository.create(NewProject("Unique", "Dr. Two"))


@pytest.mark.anyio
async def test_memory_repository_deletes_existing_project(anyio_backend):
    repository = InMemoryProjectRepository()
    project = await repository.create(NewProject("Delete me", "Dr. One"))

    assert await repository.delete(project.project_id) is True
    assert await repository.delete(project.project_id) is False
    assert await repository.list() == []
