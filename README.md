# URL Shortener with Click Analytics

A backend-focused URL shortener built incrementally with FastAPI, PostgreSQL, Redis, and Docker.

## Checkpoint 0: FastAPI foundation

This first checkpoint intentionally contains no database, authentication, Redis, or analytics. Its
purpose is to understand the application entry point, route registration, JSON responses, and the
OpenAPI documentation FastAPI generates.

## Run locally

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install and run the project:

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Visit:

- `http://localhost:8000/`
- `http://localhost:8000/api/v1/health`
- `http://localhost:8000/docs`

## Before Checkpoint 1

Be able to explain:

1. What `app = FastAPI(...)` creates.
2. What the `@app.get(...)` decorator does.
3. Why the health endpoint returns a dictionary.
4. How FastAPI generates `/docs` without us building a documentation page.

Small exercise: add a `GET /api/v1/version` endpoint returning `{"version": "0.1.0"}`.

## Roadmap

- [x] Checkpoint 0: FastAPI foundation
- [ ] Checkpoint 1: PostgreSQL connection and first SQLAlchemy model
- [ ] Checkpoint 2: Alembic and the initial migration
- [ ] Checkpoint 3: Create, list, and redirect short links
- [ ] Checkpoint 4: Click-event analytics
- [ ] Checkpoint 5: JWT authentication and link ownership
- [ ] Checkpoint 6: Custom aliases and expiry dates
- [ ] Checkpoint 7: Redis redirect cache
- [ ] Checkpoint 8: Docker and Docker Compose
- [ ] Checkpoint 9: pytest and GitHub Actions
- [ ] Checkpoint 10: Logging and API documentation polish

