DO $$
DECLARE
    id_type TEXT;
BEGIN
    SELECT data_type
    INTO id_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'projects'
      AND column_name = 'project_id';

    IF id_type IN ('integer', 'bigint') THEN
        ALTER TABLE projects
            ADD COLUMN project_id_uuid UUID NOT NULL DEFAULT gen_random_uuid();
        ALTER TABLE projects DROP COLUMN project_id;
        ALTER TABLE projects RENAME COLUMN project_id_uuid TO project_id;
        ALTER TABLE projects ADD CONSTRAINT projects_pkey PRIMARY KEY (project_id);
    END IF;
END $$;
