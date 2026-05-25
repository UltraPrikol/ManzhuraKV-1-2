class EmployeeNotFoundError(Exception):
    pass

class DepartmentNotFoundError(Exception):
    pass

class ProjectNotFoundError(Exception):
    pass

class InvalidStatusError(Exception):
    pass

class DuplicateIdError(Exception):
    pass

class DeletionError(Exception):
    """Raised when an entity cannot be deleted due to dependencies."""
    pass