from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class NewProject:
    name: str
    lead_scientist: str
    description: str | None = None


@dataclass(frozen=True)
class ProjectRecord:
    project_id: UUID
    name: str
    lead_scientist: str
    description: str | None
    created_at: datetime
    completed_at: datetime | None = None
