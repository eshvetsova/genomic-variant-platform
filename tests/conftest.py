import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_project_service
from app.core.config import Settings
from app.infrastructure.memory.projects import InMemoryProjectRepository
from app.main import create_app
from app.services.projects import ProjectService


@pytest.fixture
def memory_store():
    return InMemoryProjectRepository()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def api_client(memory_store):
    app = create_app(Settings(PROJECT_NAME="Test Genomics API"))
    app.dependency_overrides[get_project_service] = lambda: ProjectService(memory_store)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.pop(get_project_service, None)
