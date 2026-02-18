## DevSecOps Device Tracker

### Architecture

- **DeviceRegistrationAPI** (`device_registration_api`):
  - `POST /Device/register` – saves a `(userKey, deviceType)` pair to Postgres.
- **StatisticsAPI** (`statistics_api`):
  - `POST /Log/auth` – validates input and calls `DeviceRegistrationAPI`.
  - `GET /Log/auth/statistics?deviceType=...` – returns `{ deviceType, count }` or `{ deviceType, -1 }` on DB error.
- Shared **PostgreSQL** database and a small shared `common` package for `DeviceType`.

### Prerequisites

- Container engine: **Podman** or **Docker** (initially tested with Podman, but also with Docker)
- **docker-compose** or **podman-compose** (v2.x recommended)
- I didn't test it on a **MacOS** with **M chips**, so not sure on ARM64

### Configuration

1. Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
# edit .env with your own credentials if desired
```

2. Key variables:

- `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB`: Postgres credentials.
- `DATABASE_URL`: connection string used by both APIs.
- `DEVICE_REGISTRATION_API_HOST`: hostname that StatisticsAPI uses to reach DeviceRegistrationAPI (matches the compose service name by default).

### Running the stack

Using **Podman**:

```bash
podman-compose up --build
```

Using **Docker**:

```bash
docker-compose up --build
```

This starts:

- Postgres (not exposed on the host), with a named volume `postgres_data`.
- DeviceRegistrationAPI container.
- StatisticsAPI container exposed on `http://localhost:8000`.

Both API containers:

- Run as a non‑root user.
- Drop Linux capabilities and set `no-new-privileges`.
- Use a read‑only root filesystem with a writable `tmpfs` at `/tmp`.

### Example usage

1. **Register a login event** (goes through StatisticsAPI → DeviceRegistrationAPI → DB):

```bash
curl -X POST http://localhost:8000/Log/auth \
  -H "Content-Type: application/json" \
  -d '{"userKey": "user123", "deviceType": "iOS"}'
```

2. **Get statistics for a device type**:

```bash
curl "http://localhost:8000/Log/auth/statistics?deviceType=iOS"
```

### Notes

- Python dependencies are version‑pinned in each service’s `requirements.txt`
- `DATABASE_URL` is required at runtime; containers will fail fast if it is not set
- `AUTO_CREATE_TABLES=true` can be used for demo runs to create tables automatically (production would use migrations, I know its not the same but for the demo)
- This codebase is intentionally small
