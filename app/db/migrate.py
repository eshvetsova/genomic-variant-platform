import asyncio
import logging
from pathlib import Path

from sqlalchemy import text

from app.core.config import Settings
from app.db.session import create_database_resources

logger = logging.getLogger(__name__)
MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"


async def apply_migrations(connection) -> None:
    await connection.execute(
        text(
            "CREATE TABLE IF NOT EXISTS app_schema_migrations "
            "(version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())"
        )
    )

    for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
        found = await connection.scalar(
            text("SELECT 1 FROM app_schema_migrations WHERE version = :version"),
            {"version": migration.name},
        )
        if found:
            continue

        await connection.exec_driver_sql(migration.read_text())
        await connection.execute(
            text("INSERT INTO app_schema_migrations (version) VALUES (:version)"),
            {"version": migration.name},
        )
        logger.info("Database migration applied version=%s", migration.name)


async def run_migrations(database_url=None) -> None:
    resolved_url = database_url or Settings().DATABASE_URL
    engine, _ = create_database_resources(resolved_url)
    try:
        async with engine.begin() as connection:
            await apply_migrations(connection)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_migrations())
