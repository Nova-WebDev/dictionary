# CLAUDE.md — Dictionary Project

## Project overview

Email-based passwordless dictionary app. Backend: FastAPI + SQLAlchemy async + Redis + PostgreSQL. Frontend: React 19 + Vite + TypeScript. Deployed via Docker Compose with Nginx reverse proxy.

## Build & run

```bash
# Build base image first (required for backend)
docker build -t dictionary-base ./base_python

# Start all services
docker compose up --build


# Frontend dev server (runs on host, port 5173 — nginx proxies / to it)
cd front && npm run dev
```

**Service URLs (via nginx on port 80):**
- `/api/*` → backend (FastAPI on port 8000)
- `/*` → frontend (Vite dev server on host port 5173)

## Tech stack

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (async), Redis (async), PostgreSQL 16
- **Auth**: Ed25519-signed access tokens (httpOnly cookie), opaque refresh tokens in Redis
- **Frontend**: React 19, Vite 8, TypeScript 6
- **Infra**: Docker Compose (5 services: redis, postgres, backend, nginx)

## Project structure

```
back/
  main.py                   # FastAPI app (currently empty — needs wiring)
  app/
    settings.py             # Env config (pydantic-settings)
    data/                   # SQLAlchemy engine, session, Base, init_db
    redis/redis_client.py   # Async Redis client
    security/               # Access-token validation + FastAPI dependency
    key/                    # Ed25519 keypair (.pem files — currently missing)
    utils/                  # Logger, error mapper
  routers/                  # FastAPI routers (only auth_router exists)
  schemas/                  # Pydantic request/response schemas per domain
  di/                       # Manual DI factories (no framework)
  auth/                     # Auth domain (clean architecture)
    core/       → entities, errors, interfaces (ABCs), use_cases
    infrastructure/ → repos, Redis stores, SMTP sender, Ed25519 signer
  user/                     # User management domain (same structure as auth)
  dictionary/               # Dictionary domain (same structure as auth)
front/
  src/                      # React app (currently default Vite template)
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

## Auth flow

1. `POST /send-code/` — validate email (domain allowlist + blocklist), email 5-char code, store in Redis (TTL 120s, cooldown 60s)
2. `POST /verify-code/` — verify code (5 attempts max), create user if new, issue refresh token in Redis + access_token httpOnly cookie
3. `POST /refresh/` — rotate refresh token, re-check block/role state from Redis, issue new tokens
4. `POST /log-out/` — delete refresh token from Redis, clear cookie

Access tokens: Ed25519-signed, 15min TTL, httpOnly/secure/samesite=lax cookie.
Refresh tokens: opaque (secrets.token_urlsafe), stored in Redis with 30-day TTL.

## Roles

- `1` = default user
- `10` = can create words, edit/delete when author unknown
- `20` = can change other users' roles
- Block/unblock requires requester role > target role

## Database

PostgreSQL 16 with `pg_trgm` extension. GIN trigram indexes on `users.username`, `words.english_word`, `words.persian_word`. Repositories use ILIKE for search.

## Known gaps

1. `main.py` is empty — no FastAPI app, no router inclusion, no startup events
2. Only `auth_router.py` exists — user/dictionary routers not yet created
3. `app/key/` is missing `private_key.pem` and `public_key.pem`
4. `init_db.py._load_models()` is a no-op — doesn't import model modules
5. Frontend is untouched Vite template — no dictionary UI
6. Backend Python requirement mismatch (3.14 in pyproject.toml vs 3.12 base image)
7. No `/health` endpoint but compose healthcheck expects it
