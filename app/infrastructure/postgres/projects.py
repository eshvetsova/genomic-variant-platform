from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ProjectNameAlreadyExistsError
from app.domain.projects import NewProject, ProjectRecord
from app.models.project import Project
from app.repositories.projects import ProjectRepository


class SqlAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, project: NewProject) -> ProjectRecord:
        db_project = Project(
            name=project.name,
            lead_scientist=project.lead_scientist,
            description=project.description,
        )
        self.session.add(db_project)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            constraint = getattr(exc.orig, "constraint_name", None) or getattr(
                getattr(exc.orig, "diag", None), "constraint_name", None
            )
            if constraint == "uq_projects_name":
                raise ProjectNameAlreadyExistsError(project.name) from exc
            raise
        await self.session.refresh(db_project)
        return self._to_record(db_project)

    async def list(self) -> Sequence[ProjectRecord]:
        result = await self.session.scalars(select(Project).order_by(Project.project_id))
        return [self._to_record(project) for project in result.all()]

    async def delete(self, project_id: UUID) -> bool:
        project = await self.session.get(Project, project_id)
        if project is None:
            return False
        await self.session.delete(project)
        await self.session.commit()
        return True

    @staticmethod
    def _to_record(project: Project) -> ProjectRecord:
        return ProjectRecord(
            project_id=project.project_id,
            name=project.name,
            lead_scientist=project.lead_scientist,
            description=project.description,
            created_at=project.created_at,
            completed_at=project.completed_at,
        )
