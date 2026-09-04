# Alembic Guide

## What Alembic is (simply)

Alembic is a **version control system for your database schema** — think "git for tables".

- Every change to the database (add a table, add a column, rename something) is written as a **migration** file.
- Each migration has an `upgrade()` (apply the change) and a `downgrade()` (undo it).
- Migrations are **ordered** — each one points to the previous one, forming a chain.
- Alembic tracks which migrations are already applied in a special table called `alembic_version`.

Why you need it instead of `create_all()`:

| | `create_all()` | Alembic |
|---|---|---|
| Adds new tables | yes | yes |
| Adds a column to an existing table | no | yes |
| Renames/removes a column | no | yes |
| Works when team members have different DBs | no | yes |
| Can roll back a change | no | yes |

`create_all()` only creates tables that don't exist yet — it can never *change* an existing table. Alembic can.

## Core concepts

- **Migration (revision)** — one `.py` file in `alembic/versions/` describing one schema change.
- **revision id** — unique string identifying a migration (this project uses `0001`, `0002`, ...).
- **head** — the latest migration in the chain.
- **`alembic_version` table** — a single-row table in your DB storing the current revision. This is how Alembic knows what has been applied.
- **autogenerate** — Alembic compares your SQLAlchemy models against the DB and writes the migration for you (mostly).

## Install

### Local (for running alembic from your machine)

The project uses `uv`. From the `back/` directory:

```bash
cd back
uv sync          # installs everything in pyproject.toml, including alembic
alembic --version
```

(Equivalent with plain pip, if you prefer: `pip install alembic`)

### Inside Docker (for running migrations in the container)

The backend image gets its dependencies from `base_python/pyproject.toml` (already updated). Rebuild the base image, then the backend:

```bash
docker build -t dictionary-base ./base_python
docker compose build backend
```

Then run alembic inside the container:

```bash
docker compose exec backend alembic upgrade head
```

## Where things live in this project

```
back/
├── alembic.ini                 # alembic config (logging, script location)
├── alembic/
│   ├── env.py                  # connects to DB, imports your models
│   ├── script.py.mako          # template for new migration files
│   └── versions/               # the actual migration files (this is the "separate folder")
│       └── 0001_create_users_and_words.py
```

The **database URL** is read from the `DATABASE_URL` env var in `env.py` (falls back to `postgresql+asyncpg://admin:admin123@localhost:5432/dictionary` for local dev).

## Daily commands (cheatsheet)

Always run from `back/`:

```bash
# See current DB revision
alembic current

# See migration history (what's applied / pending)
alembic history

# Apply all pending migrations (upgrade to latest)
alembic upgrade head

# Apply just the next migration
alembic upgrade +1

# Roll back one migration
alembic downgrade -1

# Roll back everything
alembic downgrade base

# Create a new empty migration (you fill it in)
alembic revision -m "add word status column"

# Create a migration automatically from your models
alembic revision --autogenerate -m "add word status column"
```

## Normal workflow (adding a schema change)

1. Edit the SQLAlchemy model (e.g. add a column to `WordEntry`).
2. Generate the migration:

   ```bash
   cd back
   alembic revision --autogenerate -m "add status to words"
   ```

3. **Read the generated file** in `alembic/versions/`. Autogenerate is not perfect — check it did what you meant.
4. Apply it:

   ```bash
   alembic upgrade head
   ```

5. Commit both the model change and the new migration file.

## Team workflow (the important rules)

1. **Never edit a migration after it's been merged/pushed.** If a teammate has already run `0003`, and you change `0003` later, their DB and yours diverge forever. If a migration is wrong, write a **new** migration that fixes it.

2. **Never run migrations against a shared/production DB casually.** One person deploys migrations; everyone else just pulls.

3. **Always `git pull` before generating a migration.** If two people both create a migration that points to `0003` as its parent, you get two `0004`s — a branch in history that must be merged manually. Pull first, then generate.

4. **Every migration file must be committed** alongside the model change. A model change without its migration means teammates' DBs won't match their code.

5. **When you pull new migrations, run `alembic upgrade head`** before starting the app, or the app may query columns that don't exist yet.

## Handling an existing database (important — this project already has tables)

This project's DB was already created by `create_all()` in `app/data/init_db.py`, so the tables exist but the `alembic_version` table does not. To adopt it without re-creating tables:

```bash
alembic stamp head
```

`stamp` marks the DB as "already at head" **without running anything** — it only writes the `alembic_version` table. From then on, Alembic and the DB are in sync.

> Do NOT run `alembic upgrade head` on a DB that already has the tables — it will try to `CREATE TABLE users` and fail because it already exists.

## Resolving the `create_all()` overlap

Right now `main.py` still calls `init_db()` (which runs `create_all`) on startup. With Alembic in place, you should eventually remove that so the schema is managed only by Alembic:

- Keep `init_db()` → tables auto-created on startup, but Alembic's version table is ignored (can drift).
- Remove `init_db()` → cleaner, but fresh databases must run `alembic upgrade head` before the app starts.

Recommendation: remove `create_all` and run `alembic upgrade head` as part of startup/deploy. This is a decision for the team — flag it and pick one.

## Common pitfalls

- **"Target database is not up to date"** — you pulled new migrations but didn't run `alembic upgrade head`.
- **Autogenerate produced an empty migration** — your DB is already ahead of your models (or you forgot to import the model in `env.py`).
- **Autogenerate wants to drop/recreate everything** — usually a mismatch in column types or missing `server_default`; read the diff carefully.
- **`no such table: alembic_version` on `current`** — the DB was created by `create_all`; use `alembic stamp head`.
