from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from app.domain.projects import NewProject, ProjectRecord


class ProjectRepository(Protocol):
    async def create(self, project: NewProject) -> ProjectRecord: ...

    async def list(self) -> Sequence[ProjectRecord]: ...

    async def delete(self, project_id: UUID) -> bool: ...
