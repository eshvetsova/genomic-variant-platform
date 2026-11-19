from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    lead_scientist: str = Field(min_length=1, max_length=100)
    description: str | None = None

    @field_validator("name", "lead_scientist")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: UUID
    name: str
    lead_scientist: str
    description: str | None
    created_at: datetime
    completed_at: datetime | None


class HealthRead(BaseModel):
    status: str
    service: str
