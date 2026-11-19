import pytest
from pydantic import ValidationError

from app.schemas.project import ProjectCreate


def test_project_create_accepts_valid_payload():
    project = ProjectCreate(name="Variant cohort", lead_scientist="Dr. Ada", description="Study")
    assert project.name == "Variant cohort"
    assert project.lead_scientist == "Dr. Ada"


@pytest.mark.parametrize("field", ["name", "lead_scientist"])
def test_project_create_rejects_blank_required_text(field):
    payload = {"name": "Study", "lead_scientist": "Scientist"}
    payload[field] = "   "
    with pytest.raises(ValidationError):
        ProjectCreate(**payload)


def test_project_create_rejects_name_longer_than_database_limit():
    with pytest.raises(ValidationError):
        ProjectCreate(name="x" * 101, lead_scientist="Scientist")


def test_project_create_rejects_server_owned_fields():
    with pytest.raises(ValidationError):
        ProjectCreate(
            name="Study",
            lead_scientist="Scientist",
            project_id="00000000-0000-0000-0000-000000000001",
        )
