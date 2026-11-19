import asyncio

from pydantic import SecretStr

from app.core.config import Settings
from app.db.session import create_database_resources


def test_database_resources_configures_async_postgres_url():
    engine, session_factory = create_database_resources(
        "postgresql://user:password@localhost:5432/variants_test"
    )
    try:
        assert engine.url.drivername == "postgresql+asyncpg"
        assert session_factory.kw["expire_on_commit"] is False
    finally:
        asyncio.run(engine.dispose())


def test_database_url_is_masked_in_settings_repr():
    settings = Settings(DATABASE_URL=SecretStr("postgresql+asyncpg://user:top-secret@localhost/db"))
    assert "top-secret" not in repr(settings)
    assert str(settings.DATABASE_URL) == "**********"
