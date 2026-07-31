from app.errors import DomainError


class WordNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Word not found"):
        super().__init__(message)


class PermissionDeniedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class WordPersistenceError(DomainError):
    status_code = 500

    def __init__(self, message: str = "Failed to persist word entry"):
        super().__init__(message)
