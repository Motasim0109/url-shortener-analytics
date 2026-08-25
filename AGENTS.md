# URL Shortener with Click Analytics

## Project goal

Build a portfolio-quality backend URL shortener while learning every concept involved.

The learning process is more important than finishing quickly. The project must be built incrementally, and I must understand every dependency, command, design choice, and code change before it is introduced.

## Planned technology stack

These technologies are planned but must only be introduced when the current checkpoint requires them:

- FastAPI for the HTTP API and OpenAPI documentation
- PostgreSQL for persistent relational data
- SQLAlchemy for database access and models
- Alembic for database migrations
- JWT authentication for user accounts and link ownership
- Redis for caching short-code lookups
- Docker and Docker Compose for reproducible local infrastructure
- pytest for automated tests
- GitHub Actions for continuous integration
- Structured logging for redirects and authentication failures

Do not install, configure, or implement all of these at once.

## Current state

Checkpoint 0 is complete.

The application currently contains:

- A FastAPI application in `app/main.py`
- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/version`
- Automatically generated Swagger documentation at `/docs`
- Python and Ruff configuration in `pyproject.toml`

Do not assume later features already exist.

## Learning rules

For every new concept or change:

1. Explain what we are building.
2. Explain what problem it solves in this project.
3. Explain any new terminology.
4. Show where it fits in the application architecture.
5. Do not edit files, install dependencies, or run modifying commands until I explicitly authorize it.
6. Give me one small implementation task and let me attempt it first.
7. Review my implementation without immediately replacing it.
8. Identify what is correct before explaining what should change.
9. Prefer hints when I can reasonably discover the solution.
10. Provide the direct solution only after I attempt it or explicitly request it.
11. Explain every command before asking me to run it.
12. Work on only one checkpoint and one small task at a time.
13. Do not generate future features early.
14. Do not introduce abstractions merely because they might be useful later.
15. Before advancing, ask me to explain the main concept in my own words.
16. End each completed checkpoint with validation and a focused Git commit.

If I ask a conceptual question, answer it before continuing implementation.

If I paste code, review that code rather than rewriting the entire file.

If an error occurs, help me understand the error message and diagnose the cause before applying a fix.

## Implementation roadmap

Follow this sequence:

1. Checkpoint 0: FastAPI foundation
2. Checkpoint 1: PostgreSQL, configuration, engine, connection, and session concepts
3. Checkpoint 2: First SQLAlchemy model and initial Alembic migration
4. Checkpoint 3: Create and list short links
5. Checkpoint 4: Generate short codes and implement redirects
6. Checkpoint 5: Record click events and expose analytics
7. Checkpoint 6: User signup, login, JWT authentication, and link ownership
8. Checkpoint 7: Custom aliases and expiry dates through Alembic migrations
9. Checkpoint 8: Redis redirect caching and cache invalidation
10. Checkpoint 9: Docker and Docker Compose
11. Checkpoint 10: pytest test suite
12. Checkpoint 11: GitHub Actions, structured logging, and API documentation polish

Do not move to another checkpoint until the current checkpoint is understood, validated, and committed.

## Engineering conventions

- Use Python 3.13.
- Use type hints for functions.
- Prefer clear, explicit code over clever code.
- Avoid unnecessary design patterns and premature abstractions.
- Keep secrets and machine-specific configuration out of Git.
- Use environment variables for configuration when they become necessary.
- Do not create database tables with `Base.metadata.create_all()`.
- Once tables are introduced, use Alembic migrations as the source of truth.
- Keep API routes under `/api/v1`, except public short-link redirects.
- Explain new folders and files before creating them.

## Current validation commands

Explain each command before using it.

Run the application:

`uvicorn app.main:app --reload`

Check linting:

`ruff check .`

Check formatting:

`ruff format --check .`

Do not add testing commands until pytest is introduced.

## Git workflow

- Keep commits small and focused on one checkpoint or coherent sub-step.
- Review the diff before committing.
- Explain what each commit contains.
- Do not mix unrelated changes.
- Do not push or create a pull request without my explicit permission.