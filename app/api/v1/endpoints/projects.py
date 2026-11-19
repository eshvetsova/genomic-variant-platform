from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_project_service
from app.domain.errors import ProjectNameAlreadyExistsError, ProjectNotFoundError
from app.schemas.project import ProjectCreate, ProjectRead
from app.services.projects import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate, service: ProjectService = Depends(get_project_service)
) -> ProjectRead:
    try:
        record = await service.create_project(**project.model_dump())
    except ProjectNameAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A project with this name already exists",
        ) from exc
    return ProjectRead.model_validate(record)


@router.get("/", response_model=list[ProjectRead])
async def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectRead]:
    return [ProjectRead.model_validate(project) for project in await service.list_projects()]


@router.delete("/{project_id}/", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_project(
    project_id: UUID, service: ProjectService = Depends(get_project_service)
) -> Response:
    try:
        await service.delete_project(project_id)
    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
