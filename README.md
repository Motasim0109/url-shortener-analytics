# URL Shortener with Click Analytics

A backend-focused URL shortener built incrementally with FastAPI, PostgreSQL, Redis, and Docker.

The project is built one backend concept at a time, with manual validation at each checkpoint.

## Features

- User signup and login with hashed passwords and JWT authentication.
- Authenticated link creation, owner-filtered link listing, and private click analytics.
- Public redirects with custom aliases and optional expiration dates.
- PostgreSQL storage with Alembic migrations and a click event for each successful redirect.
- Redis redirect caching with expiration-aware TTLs and PostgreSQL fallback on Redis errors.

## Run with Docker Compose

Start Docker Desktop with the Linux container engine running. Run the commands below from the
project root. Python and the service dependencies run inside containers, so a host Python virtual
environment is not needed for this workflow.

Create or update `.env` beside `compose.yaml`, preserving any existing local settings:

```dotenv
JWT_SECRET_KEY=replace_with_a_random_secret
POSTGRES_PASSWORD=replace_with_a_random_hex_password
```

Replace both placeholders with independently generated random values. Use a long random JWT secret
(for example, 32 random bytes represented as 64 hexadecimal characters). Use a random hexadecimal
database password because Compose embeds it in a connection URL. Other passwords may require URL
encoding. Keep `.env` private; it is excluded from Git and the Docker build context.

Compose supplies the API's `DATABASE_URL` and `REDIS_URL` using the internal service names `db` and
`redis`. The container database is separate from your Windows PostgreSQL database; existing Windows
users and links are not copied into it.

Build the API image, start its dependencies, apply migrations, and start the API:

```powershell
docker compose build api
docker compose up -d db redis
docker compose run --rm api alembic upgrade head
docker compose up -d api
```

The migration command runs in a temporary API container and removes that container afterward.
PostgreSQL data remains in the named volume. The API waits for PostgreSQL's readiness check, but
that check does not apply migrations; the migration step is still required.

If another application is using port `8000`, stop it before starting the API container.

Visit [the API documentation](http://127.0.0.1:8000/docs) or
[the health endpoint](http://127.0.0.1:8000/api/v1/health).
On a fresh database, sign up and log in through the API to create your first user and access token.
Only the API port is published to Windows; PostgreSQL and Redis communicate over the Compose network.

## Everyday Commands

Start an already initialized stack:

```powershell
docker compose up -d
```

After changing Python code or dependencies, rebuild the image and update the running API:

```powershell
docker compose up -d --build
```

The image contains a copy of the project from build time. Restarting a container alone does not
copy in code changes. If a change includes new migrations, build the image and apply those
migrations before updating the API, using the first-time startup sequence above.

Inspect container status and recent API logs:

```powershell
docker compose ps
docker compose logs --tail 50 api
```

Validate the Compose configuration without printing resolved secrets:

```powershell
docker compose config --quiet
```

Stop and remove this project's containers and network while retaining its named database volume:

```powershell
docker compose down
```

The `postgres_data` volume preserves users, links, and click events across container replacement.
Do not add `--volumes` to the shutdown command unless you intend to delete that database storage.
Redis holds rebuildable cache data; PostgreSQL is the source of truth.

PostgreSQL's initialization settings apply when its volume is empty. Changing `POSTGRES_PASSWORD`
in `.env` later does not change the password stored in an existing database.

## Roadmap

- [x] Checkpoint 0: FastAPI foundation
- [x] Checkpoint 1: PostgreSQL configuration, engine, and sessions
- [x] Checkpoint 2: First SQLAlchemy model and initial Alembic migration
- [x] Checkpoint 3: Generate, create, and list short links
- [x] Checkpoint 4: Short-code collision handling and redirects
- [x] Checkpoint 5: Click events and analytics
- [x] Checkpoint 6: Signup, login, JWT authentication, and link ownership
- [x] Checkpoint 7: Custom aliases and expiration dates
- [x] Checkpoint 8: Redis redirect caching and invalidation
- [ ] Checkpoint 9: Docker and Docker Compose (validated; checkpoint commit pending)
- [ ] Checkpoint 10: pytest test suite
- [ ] Checkpoint 11: GitHub Actions, structured logging, and API documentation polish
