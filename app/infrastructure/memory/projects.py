from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.errors import ProjectNameAlreadyExistsError
from app.domain.projects import NewProject, ProjectRecord
from app.repositories.projects import ProjectRepository


class InMemoryProjectRepository(ProjectRepository):
    def __init__(self):
        self._projects: dict[UUID, ProjectRecord] = {}

    async def create(self, project: NewProject) -> ProjectRecord:
        if any(existing.name == project.name for existing in self._projects.values()):
            raise ProjectNameAlreadyExistsError(project.name)

        record = ProjectRecord(
            project_id=uuid4(),
            name=project.name,
            lead_scientist=project.lead_scientist,
            description=project.description,
            created_at=datetime.now(timezone.utc),
        )
        self._projects[record.project_id] = record
        return record

    async def list(self) -> list[ProjectRecord]:
        return list(self._projects.values())

    async def delete(self, project_id: UUID) -> bool:
        return self._projects.pop(project_id, None) is not None
