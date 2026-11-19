CREATE TABLE IF NOT EXISTS projects (
    project_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lead_scientist VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    CONSTRAINT uq_projects_name UNIQUE (name)
);
