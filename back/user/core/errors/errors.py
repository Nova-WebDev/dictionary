class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class PermissionDeniedError(Exception):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class InvalidRoleError(Exception):
    def __init__(self, message: str = "Invalid role value"):
        super().__init__(message)


class UsernameUpdateError(Exception):
    def __init__(self, message: str = "Failed to update username"):
        super().__init__(message)