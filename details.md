# Dictionary Project — Architecture & Details

## File structure

```
dictionary/
├── docker-compose.yml
├── .gitignore
├── base_python/
│   ├── Dockerfile              # python:3.12-slim + uv + Cairo/Pango libs → image "dictionary-base"
│   └── pyproject.toml          # base dependency set
├── back/
│   ├── main.py                 # FastAPI app entry point (EMPTY — 0 bytes)
│   ├── pyproject.toml          # Dependencies (requires-python >= 3.14, mismatch with base)
│   ├── uv.lock                 # Pinned dependency versions
│   ├── Dockerfile              # FROM dictionary-base, copies source
│   ├── .dockerignore
│   ├── app/
│   │   ├── __init__.py
│   │   ├── settings.py         # Pydantic-settings: DATABASE_URL, REDIS_URL, SMTP creds, etc.
│   │   ├── data/
│   │   │   ├── base.py         # SQLAlchemy DeclarativeBase
│   │   │   ├── db.py           # Async engine + session factory + get_session dependency
│   │   │   └── init_db.py      # create_all + _load_models (no-op, missing imports)
│   │   ├── redis/
│   │   │   └── redis_client.py # Async Redis client singleton
│   │   ├── security/
│   │   │   ├── dependencies.py # get_current_user FastAPI dependency
│   │   │   └── token_validator.py # Ed25519 public-key token validation
│   │   ├── key/
│   │   │   └── __init__.py     # Directory for private_key.pem / public_key.pem (MISSING)
│   │   └── utils/
│   │       ├── logger.py       # Structlog logger
│   │       └── error_mapper.py # Domain error → HTTP response mapping
│   ├── routers/
│   │   ├── __init__.py
│   │   └── auth_router.py      # Auth endpoints (ONLY router implemented)
│   ├── schemas/
│   │   ├── auth/               # send_code, verify_code, refresh, logout schemas
│   │   ├── user/               # user_profile, user_list, update_username, role, block schemas
│   │   └── dictionary/         # word_create, word_update, word_detail, word_list schemas
│   ├── di/
│   │   ├── auth_providers.py          # Auth use-case factories
│   │   ├── cross_domain_providers.py  # Cross-domain wiring (block→token revoke, role sync)
│   │   ├── dictionary_providers.py    # Dictionary use-case factories
│   │   └── user_providers.py          # User use-case factories
│   ├── auth/
│   │   ├── core/
│   │   │   ├── entities/       # RefreshToken, TokenHeader, TokenPayload, UserIdentity,
│   │   │   │                   #   UserBlockStatus, UserRoleUpdate (all dataclasses)
│   │   │   ├── errors/errors.py
│   │   │   ├── interfaces/     # 13 ABCs/Protocols: repositories, stores, signer, sender
│   │   │   └── use_cases/      # send_code, verify_code, refresh_token, logout,
│   │   │                       #   check_user_blocked, revoke_user_tokens, update_user_role_in_tokens
│   │   ├── infrastructure/
│   │   │   ├── data/           # EmailBlockRepository, UserRepository (SQLAlchemy)
│   │   │   ├── email/          # EmailSender (SMTP/Gmail), EmailTemplate
│   │   │   ├── signing/        # TokenHeaderGenerator, TokenPayloadGenerator, TokenSigner (Ed25519)
│   │   │   └── store/          # Redis-backed: AttemptCounter, BlockService,
│   │   │                       #   CodeStore, RefreshTokenStore, UserRemoveStore, UserRoleStore
│   │   └── utility/            # base64url, code_generator, secure_token_generator
│   ├── user/
│   │   ├── core/
│   │   │   ├── entities/       # User, UserSummary (dataclasses)
│   │   │   ├── errors/errors.py
│   │   │   ├── interfaces/     # IUserRepository (ABC), IUserLookup (Protocol)
│   │   │   └── use_cases/      # get_user_profile, get_all_users, update_username,
│   │   │                       #   change_role, toggle_block
│   │   └── infrastructure/
│   │       └── data/           # User model (SQLAlchemy), UserRepository
│   └── dictionary/
│       ├── core/
│       │   ├── entities/       # WordEntry, WordSummary (dataclasses)
│       │   ├── errors/errors.py
│       │   ├── interfaces/     # IWordRepository (ABC), IUserLookup (Protocol)
│       │   └── use_cases/      # search_words, get_words_paginated, create_word,
│       │                       #   update_word, delete_word
│       └── infrastructure/
│           └── data/           # WordEntry model (SQLAlchemy), WordRepository
├── nginx/
│   ├── Dockerfile              # nginx:stable
│   └── nginx.conf              # /api/ → backend:8000, / → host.docker.internal:5173
├── postgresql/
│   ├── Dockerfile              # postgres:16
│   └── init.sql                # CREATE DATABASE dictionary + CREATE EXTENSION pg_trgm
└── front/
    ├── package.json            # React 19, Vite 8, TypeScript 6
    ├── vite.config.ts          # Default React plugin (no API proxy)
    ├── index.html
    └── src/
        ├── main.tsx
        ├── App.tsx             # Default Vite starter template (counter demo)
        ├── App.css
        └── index.css
```

## Architecture

The backend follows **Clean Architecture / Hexagonal** pattern, organized into three bounded contexts:

### Domain: `auth`
Passwordless email-based authentication.

**Entities**: `RefreshToken`, `TokenHeader`, `TokenPayload`, `UserIdentity`, `UserBlockStatus`, `UserRoleUpdate`

**Interfaces (ABCs)**: `IEmailBlockRepository`, `IUserRepository`, `ICodeStore`, `IAttemptCounter`, `IBlockService`, `IRefreshTokenStore`, `ITokenSigner`, `ITokenHeaderGenerator`, `ITokenPayloadGenerator`, `IUserRemoveStore`, `IUserRoleStore`, `IEmailSender`, `ISecureTokenGenerator`, `ICodeGenerator`

**Use cases**:
- `send_code` — validate email, check blocklist, send verification code
- `verify_code` — verify code, create user if new, issue tokens
- `refresh_token` — rotate refresh token, re-check block/role state
- `logout` — delete refresh token, clear cookie
- `check_user_blocked` — Redis lookup for blocked users
- `revoke_user_tokens` — invalidate all refresh tokens for a user
- `update_user_role_in_tokens` — sync role changes to Redis

**Infrastructure adapters**: SQLAlchemy repos, Redis stores (code, attempts, blocks, refresh tokens, user remove/role), SMTP email sender (Gmail), Ed25519 token signer

### Domain: `user`
User management and administration.

**Entities**: `User` (id, public_id, username, email, role, is_blocked, created_at), `UserSummary`

**Interfaces**: `IUserRepository` (full CRUD + paginated list + search + role/block updates), `IUserLookup` (read-only, used cross-domain)

**Use cases**: `get_user_profile`, `get_all_users`, `update_username`, `change_role`, `toggle_block`

**Infrastructure**: SQLAlchemy `User` model + `UserRepository`

### Domain: `dictionary`
Persian↔English word dictionary.

**Entities**: `WordEntry` (id, public_id, english, persian, author_id, status, created_at), `WordSummary`

**Interfaces**: `IWordRepository` (CRUD + paginated list + search + directional search), `IUserLookup` (for author permissions)

**Use cases**: `search_words`, `get_words_paginated`, `create_word`, `update_word`, `delete_word`

**Infrastructure**: SQLAlchemy `WordEntry` model + `WordRepository`

### Cross-domain wiring (`di/cross_domain_providers.py`)

- Blocking a user writes `auth:user_remove:{public_id}` to Redis → all refresh tokens invalidated
- Role changes write `auth:user_role:{public_id}` to Redis → next refresh picks up new role
- Dictionary mutations call `IUserLookup` to enforce author-based permissions

## API endpoints

### Implemented (auth_router.py — requires mounting in main.py)

| Method | Path | Handler | Description |
|--------|------|---------|-------------|
| POST | `/auth/send-code/` | `send_code` | Validates email, sends 5-char verification code |
| POST | `/auth/verify-code/` | `verify_code` | Verifies code (5 attempts max), creates user if new, returns refresh token + sets access_token cookie |
| POST | `/auth/refresh/` | `refresh_token` | Rotates refresh token, issues new access cookie + refresh token |
| POST | `/auth/log-out/` | `logout` | Deletes refresh token from Redis, clears cookie |

### Planned (domain logic + schemas + DI exist, routers not written)

**User management:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/users/me/` | Get own profile |
| GET | `/users/{public_id}/` | Get user by public ID |
| GET | `/users/` | Paginated user list (with search, ordering, include_self option) |
| PATCH | `/users/{public_id}/username/` | Update username |
| PATCH | `/users/{public_id}/role/` | Change user role (requires role >= 20) |
| PATCH | `/users/{public_id}/block/` | Toggle block/unblock |

**Dictionary:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/dictionary/` | Paginated word list (with author name, search filter) |
| GET | `/dictionary/search/` | Directional search (Persian→English, English→Persian) |
| POST | `/dictionary/` | Create new word entry (role >= 10) |
| PATCH | `/dictionary/{public_id}/` | Update word (author or role >= 10 if no author) |
| DELETE | `/dictionary/{public_id}/` | Delete word (author or role >= 10 if no author) |

## Features

### Authentication
- Passwordless email-based login (verification codes)
- Ed25519-signed access tokens in httpOnly cookies (15min TTL)
- Opaque refresh tokens in Redis (30-day TTL)
- Refresh token rotation with immediate revocation
- Automatic token invalidation on user block or role change
- Configurable email-domain allowlist (default: gmail.com)
- Email blocklist stored in PostgreSQL

### Rate limiting & abuse protection
- 60s cooldown between code sends per email
- 5 verification attempts per code, then 300s block
- Redis-backed counters and block state

### User management
- Paginated user listing with ILIKE search and ordering
- Username updates
- Role-based permissions (1=user, 10=contributor, 20=admin)
- Block/unblock with role hierarchy enforcement

### Dictionary
- Search: Persian→English and English→Persian
- Paginated word listing with author name join
- Create/edit/delete with author-based access control
- PostgreSQL pg_trgm extension for trigram indexes
- GIN indexes on english_word and persian_word columns

### Database
- PostgreSQL 16 with pg_trgm extension
- Trigram GIN indexes for efficient ILIKE search

## Docker / Compose

### Services

| Service | Image/Build | Port | Notes |
|---------|-------------|------|-------|
| `redis` | `redis:7-alpine` | — | 256mb, allkeys-lru, healthcheck via ping |
| `postgres` | `./postgresql` (postgres:16) | 5432 | DB: `dictionary`, user: `admin`, volume: `dictionary_pg_data` |
| `backend` | `./back` (FROM dictionary-base) | 8000 | Gunicorn + UvicornWorker, depends on postgres + redis |
| `nginx` | `./nginx` (nginx:stable) | 80 | Proxies /api/ to backend, / to host Vite on 5173 |

### Build prerequisites
1. Build base image: `docker build -t dictionary-base ./base_python`
2. Generate Ed25519 keypair into `back/app/key/`
3. Wire up `main.py` with FastAPI app and router inclusion

### Nginx routing

```
/api/*  → http://backend:8000        (strip /api prefix)
/*      → http://host.docker.internal:5173  (Vite dev server on host)
```

## Known issues

1. **`main.py` is empty** — no FastAPI app, no router inclusion, no startup/init_db call. Backend won't start.
2. **Missing Ed25519 keys** — `app/key/` has no `.pem` files; any token operation will crash with `FileNotFoundError`.
3. **No user/dictionary routers** — domain logic, schemas, and DI are complete, but no HTTP layer.
4. **`init_db._load_models()` is a no-op** — model modules not imported; `create_all` creates nothing.
5. **Python version mismatch** — `back/pyproject.toml` requires >= 3.14, but base Docker image is 3.12.
6. **Frontend is default Vite template** — no dictionary UI, no API client, no routing.
7. **No `/health` endpoint** — compose healthcheck expects `GET /health` but no route defined.
8. **Hardcoded secrets** — Gmail app password and DB credentials in `docker-compose.yml`.
9. **`secure=True` on cookie** — won't work over HTTP on localhost; needs HTTPS termination or conditional flag.
10. **`dictionary-base` image not in compose** — must be built manually before `docker compose up --build`.
