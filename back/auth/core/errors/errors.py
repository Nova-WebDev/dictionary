class TokenGenerationError(Exception):
    def __init__(self, message: str = "Failed to generate access token"):
        super().__init__(message)

class RefreshTokenPersistenceError(Exception):
    def __init__(self, message: str = "Failed to persist refresh token"):
        super().__init__(message)

class InvalidRefreshTokenError(Exception):
    def __init__(self, message: str = "Invalid or expired refresh token"):
        super().__init__(message)

class UserBlockedError(Exception):
    def __init__(self, message: str = "User is blocked"):
        super().__init__(message)

class UserStatePersistenceError(Exception):
    def __init__(self, message: str = "Failed to access user state store"):
        super().__init__(message)

class InvalidEmailFormatError(Exception):
    def __init__(self, message: str = "Invalid email format"):
        super().__init__(message)


class EmailDomainNotAllowedError(Exception):
    def __init__(self, message: str = "Email domain not allowed"):
        super().__init__(message)


class EmailBlockedError(Exception):
    def __init__(self, message: str = "Email is blocked"):
        super().__init__(message)

class EmailBlockCheckError(Exception):
    def __init__(self, message: str = "Failed to check email block status"):
        super().__init__(message)

class EmailTemporarilyBlockedError(Exception):
    def __init__(self, message: str = "Email temporarily blocked"):
        super().__init__(message)

class UserCreationError(Exception):
    def __init__(self, message: str = "Failed to create user"):
        super().__init__(message)

class InvalidVerificationCodeError(Exception):
    def __init__(self, message: str = "Invalid verification code"):
        super().__init__(message)