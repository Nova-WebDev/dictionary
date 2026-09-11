# CLAUDE.md — Dictionary Project

## Project overview

Email-based passwordless dictionary app (Persian↔English words). Backend: FastAPI + SQLAlchemy async + Redis + PostgreSQL with clean architecture. Frontend: React 19 SPA. Deployed via Docker Compose with Nginx reverse proxy.

## Build & run

```bash
# Build base image first (required for backend)
docker build -t dictionary-base ./base_python

# Start all services (backend image runs `alembic upgrade head` before gunicorn)
docker compose up --build -d

# Frontend dev server (runs on host, port 5173 — nginx proxies / to it)
cd front && npm run dev
```

**Service URLs (via nginx on port 80):**
- `/*` → frontend (Vite dev server on host port 5173)
- `/api/*` → backend (prefix stripped; FastAPI sets `root_path="/api"` so Swagger resolves paths correctly)
- `/docs`, `/redoc`, `/openapi.json` → backend (Swagger UI — no `/api` prefix needed)

## Tech stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Redis (async), PostgreSQL 16, Alembic, uv
- **Auth**: Ed25519-signed access tokens (httpOnly cookie), opaque refresh tokens in Redis
- **Frontend**: React 19, Vite 8, TypeScript 6, React Router 7, TanStack Query 5, Zustand 5, Axios, Tailwind 4
- **Infra**: Docker Compose (services: redis, postgres, backend, nginx)

## Project structure

```
back/
  main.py                   # FastAPI app: lifespan, DomainError handler, /health, routers, root_path
  alembic.ini               # Alembic config (run from back/)
  alembic/
    env.py                  # async env, reads DATABASE_URL, imports all models
    versions/               # migrations (0001_create_users_and_words, 0002_add_address_to_users)
  app/
    settings.py             # Env config (pydantic-settings)
    errors.py               # DomainError base (status_code) — all domain errors inherit it
    data/                   # SQLAlchemy engine, session factory, Base
    redis/redis_client.py   # Async Redis client
    security/               # get_current_user dependency + Ed25519 token validator
    key/                    # Ed25519 keypair PEM files (generated locally, baked into image)
    utils/logger.py         # Logger
  routers/                  # auth_router, user_router, dictionary_router
  schemas/                  # Pydantic request/response schemas per domain
  di/                       # Manual DI factories (no framework)
  auth/                     # Auth domain (clean architecture)
    core/       → entities, errors, interfaces (ABCs), use_cases
    infrastructure/ → repos, Redis stores, SMTP sender, Ed25519 signer
  user/                     # User management domain (same structure as auth)
  dictionary/               # Dictionary domain (same structure as auth)
docs/
  alembic_guide.md          # Migrations workflow (team rules, stamping, pitfalls)
  error-handling.md         # DomainError pattern
front/src/
  app/                      # App providers, root layout, routes
  auth/                     # EmailPage, VerifyPage, hooks, token refresh scheduler
  dictionary/               # DictionaryPage, word CRUD components/hooks
  user/                     # UserPage, role/block actions, CurrentUserProvider
  shared/                   # Axios instance, theme, layout, header/sidebar
  base/                     # Reusable UI: Table, Modal, Loader, etc.
postgresql/init.sql         # Creates `dictionary` DB + pg_trgm extension
nginx/nginx.conf            # Reverse proxy config
base_python/                # Base Docker image (Python + uv + system deps)
```

## Architecture pattern

Clean / hexagonal architecture per domain. Each domain (`auth`, `user`, `dictionary`) is split into:
- **`core/`** — pure Python, no I/O: entities (dataclasses), interfaces (ABCs/Protocols), use cases, errors
- **`infrastructure/`** — I/O adapters: SQLAlchemy repos, Redis stores, SMTP sender, Ed25519 signer
- **`di/`** in `back/di/` — factory functions wiring infrastructure into use cases

Data flow: `router → DI factory → use case → interface (ABC) → infrastructure → Postgres/Redis/SMTP`

**Error handling**: every domain error inherits `app.errors.DomainError` and sets a `status_code`. A single FastAPI exception handler in `main.py` converts it to JSON and logs 5xx. Adding an error = defining one new class — no mapper to edit. See `docs/error-handling.md`.

**Migrations**: Alembic owns the schema (`create_all` was removed). The backend image runs `alembic upgrade head` automatically before gunicorn. New migration = model change + `alembic revision --autogenerate`. See `docs/alembic_guide.md`.

## Auth flow (external paths `/api/auth/...`)

1. `POST /api/auth/send-code/` — validate email (domain allowlist + blocklist), email 5-char code, store in Redis (TTL 120s, cooldown 60s)
2. `POST /api/auth/verify-code/` — verify code (5 attempts max), create user if new, issue refresh token in Redis + access_token httpOnly cookie
3. `POST /api/auth/refresh/` — rotate refresh token, re-check block/role state from Redis, issue new tokens
4. `POST /api/auth/log-out/` — delete refresh token from Redis, clear cookie

Access tokens: Ed25519-signed, 15min TTL, httpOnly/secure/samesite=lax cookie. Payload: email, public_id, role, iat, exp.
Refresh tokens: opaque (secrets.token_urlsafe), stored in Redis with 30-day TTL.

## Roles

- `1` = default user
- `10` = can create words, edit/delete when author unknown
- `20` = admin: change roles, block/unblock, create users (can assign roles 1–19, cannot create another admin)
- Block/unblock requires requester role > target role

## Database

PostgreSQL 16 with `pg_trgm` extension. GIN trigram indexes on `users.username`, `words.english_word`, `words.persian_word`. Repositories use ILIKE for search. Schema changes go through Alembic migrations only.

## Known issues

1. `back/pyproject.toml` requires Python >= 3.14 while the base image is Python 3.12 — harmless today (the image build only uses `base_python/pyproject.toml`), but the files should agree.
2. Secrets are hardcoded in `docker-compose.yml` (Gmail app password, DB password) — should move to a `.env` file.
3. The access-token cookie is `secure=True`: works on `http://localhost` (browser exception), but login will silently fail if the app is opened via a LAN IP over plain HTTP.
