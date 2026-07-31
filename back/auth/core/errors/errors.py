from app.errors import DomainError


class TokenGenerationError(DomainError):
    status_code = 500

    def __init__(self, message: str = "Failed to generate access token"):
        super().__init__(message)


class RefreshTokenPersistenceError(DomainError):
    status_code = 500

    def __init__(self, message: str = "Failed to persist refresh token"):
        super().__init__(message)


class InvalidRefreshTokenError(DomainError):
    status_code = 401

    def __init__(self, message: str = "Invalid or expired refresh token"):
        super().__init__(message)


class UserBlockedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "User is blocked"):
        super().__init__(message)


class UserStatePersistenceError(DomainError):
    status_code = 500

    def __init__(self, message: str = "Failed to access user state store"):
        super().__init__(message)


class InvalidEmailFormatError(DomainError):
    status_code = 400

    def __init__(self, message: str = "Invalid email format"):
        super().__init__(message)


class EmailDomainNotAllowedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Email domain not allowed"):
        super().__init__(message)


class EmailBlockedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Email is blocked"):
        super().__init__(message)


class EmailBlockCheckError(DomainError):
    status_code = 500

    def __init__(self, message: str = "Failed to check email block status"):
        super().__init__(message)


class EmailTemporarilyBlockedError(DomainError):
    status_code = 429

    def __init__(self, message: str = "Email temporarily blocked"):
        super().__init__(message)


class UserCreationError(DomainError):
    status_code = 500

    def __init__(self, message: str = "Failed to create user"):
        super().__init__(message)


class InvalidVerificationCodeError(DomainError):
    status_code = 401

    def __init__(self, message: str = "Invalid verification code"):
        super().__init__(message)
