class WordNotFoundError(Exception):
    def __init__(self, message: str = "Word not found"):
        super().__init__(message)


class PermissionDeniedError(Exception):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class WordPersistenceError(Exception):
    def __init__(self, message: str = "Failed to persist word entry"):
        super().__init__(message)