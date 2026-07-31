class DomainError(Exception):
    status_code: int = 500

    def __init__(self, message: str = "Internal error"):
        super().__init__(message)
