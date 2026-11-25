from sqlalchemy.exc import IntegrityError

from app.infrastructure.postgres.projects import _constraint_name


def test_constraint_name_finds_wrapped_asyncpg_error():
    asyncpg_error = Exception("duplicate key")
    asyncpg_error.constraint_name = "uq_projects_name"
    sqlalchemy_wrapper = Exception("wrapped asyncpg error")
    sqlalchemy_wrapper.__cause__ = asyncpg_error
    integrity_error = IntegrityError("INSERT", {}, sqlalchemy_wrapper)

    assert _constraint_name(integrity_error) == "uq_projects_name"


def test_constraint_name_returns_none_for_other_integrity_errors():
    integrity_error = IntegrityError("INSERT", {}, Exception("foreign key failure"))

    assert _constraint_name(integrity_error) is None
