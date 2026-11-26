import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI

from app.api.v1.endpoints.projects import router as projects_router
from app.core.config import Settings
from app.core.logging_config import configure_logging
from app.db.session import create_database_resources
from app.schemas.project import HealthRead


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        configure_logging()
        engine, session_factory = create_database_resources(app_settings.DATABASE_URL)
        app.state.engine = engine
        app.state.session_factory = session_factory
        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(
        title=app_settings.PROJECT_NAME,
        openapi_url=f"{app_settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(projects_router, prefix=app_settings.API_V1_STR)
    request_logger = logging.getLogger("app.requests")

    @app.middleware("http")
    async def log_request(request, call_next):
        started = perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = (perf_counter() - started) * 1000
            level = (
                logging.ERROR
                if status_code >= 500
                else logging.WARNING
                if status_code >= 400
                else logging.INFO
            )
            request_logger.log(
                level,
                "HTTP request method=%s path=%s status=%d duration_ms=%.2f",
                request.method,
                request.url.path,
                status_code,
                duration_ms,
            )

    @app.get(
        "/health",
        tags=["Health Check"],
        status_code=200,
        response_model=HealthRead,
    )
    def health_check() -> HealthRead:
        return HealthRead(status="healthy", service=app_settings.PROJECT_NAME)

    return app
