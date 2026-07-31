# Error handling

## Approach

All domain exceptions inherit from a single base class `DomainError` that carries an HTTP `status_code`. A single FastAPI exception handler catches `DomainError` and returns a JSON response with the appropriate status code and message.

## Structure

```
app/errors.py                          # DomainError base (status_code + message)
  ├── auth/core/errors/errors.py       # 12 auth errors (400, 401, 403, 429, 500)
  ├── user/core/errors/errors.py       # 4 user errors  (400, 403, 404, 500)
  ├── dictionary/core/errors/errors.py # 3 word errors  (403, 404, 500)
  └── app/security/token_validator.py  # TokenValidationError (401)

main.py                                # @app.exception_handler(DomainError)
```

## How it works

1. Domain errors inherit from `DomainError` and set a class-level `status_code`.
2. Use cases raise domain errors directly — no HTTP knowledge in domain logic.
3. Routers call use cases **without try/except** — errors bubble up naturally.
4. FastAPI's exception handler catches `DomainError`, logs 500s, and returns a `JSONResponse`.

## Open-Closed Principle

Adding a new error requires **one change**: define a new class with a `status_code`.

```python
class NewFeatureError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Something went wrong"):
        super().__init__(message)
```

No need to modify a central mapper, handler, or router.

## Status code reference

### Auth domain

| Exception | HTTP |
|-----------|------|
| `InvalidEmailFormatError` | 400 |
| `InvalidRefreshTokenError` | 401 |
| `InvalidVerificationCodeError` | 401 |
| `UserBlockedError` | 403 |
| `EmailDomainNotAllowedError` | 403 |
| `EmailBlockedError` | 403 |
| `EmailTemporarilyBlockedError` | 429 |
| `TokenGenerationError` | 500 |
| `RefreshTokenPersistenceError` | 500 |
| `UserStatePersistenceError` | 500 |
| `EmailBlockCheckError` | 500 |
| `UserCreationError` | 500 |

### User domain

| Exception | HTTP |
|-----------|------|
| `InvalidRoleError` | 400 |
| `PermissionDeniedError` | 403 |
| `UserNotFoundError` | 404 |
| `UsernameUpdateError` | 500 |

### Dictionary domain

| Exception | HTTP |
|-----------|------|
| `PermissionDeniedError` | 403 |
| `WordNotFoundError` | 404 |
| `WordPersistenceError` | 500 |

### Security

| Exception | HTTP |
|-----------|------|
| `TokenValidationError` | 401 |

## What was removed

`app/utils/error_mapper.py` — a function with a long `isinstance` chain that mapped each error to an `HTTPException`. It violated OCP because every new error required editing the mapper. The single exception handler replaces it entirely.
