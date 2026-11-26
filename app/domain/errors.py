class ProjectNotFoundError(Exception):
    """Raised when a project lookup or deletion targets a missing project."""


class ProjectNameAlreadyExistsError(Exception):
    """Raised when a project name conflicts with an existing project."""
