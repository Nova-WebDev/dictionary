from app.errors import DomainError


class UserNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class PermissionDeniedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class InvalidRoleError(DomainError):
    status_code = 400

    def __init__(self, message: str = "Invalid role value"):
        super().__init__(message)


class UsernameUpdateError(DomainError):
    status_code = 500

    def __init__(self, message: str = "Failed to update username"):
        super().__init__(message)
