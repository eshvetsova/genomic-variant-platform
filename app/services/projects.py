import logging
from collections.abc import Sequence
from uuid import UUID

from app.domain.errors import ProjectNotFoundError
from app.domain.projects import NewProject, ProjectRecord
from app.repositories.projects import ProjectRepository

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(
        self, name: str, lead_scientist: str, description: str | None = None
    ) -> ProjectRecord:
        project = NewProject(
            name=name.strip(),
            lead_scientist=lead_scientist.strip(),
            description=description,
        )
        created = await self.repository.create(project)
        logger.info("Project created project_id=%s", created.project_id)
        return created

    async def list_projects(self) -> Sequence[ProjectRecord]:
        return await self.repository.list()

    async def delete_project(self, project_id: UUID) -> None:
        if not await self.repository.delete(project_id):
            raise ProjectNotFoundError(project_id)
        logger.info("Project deleted project_id=%s", project_id)
