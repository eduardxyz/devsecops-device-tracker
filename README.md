## DevSecOps Device Tracker

### Architecture

- **DeviceRegistrationAPI** (`device_registration_api`):
  - `POST /Device/register` – saves a `(userKey, deviceType)` pair to Postgres.
- **StatisticsAPI** (`statistics_api`):
  - `POST /Log/auth` – validates input and calls `DeviceRegistrationAPI`.
  - `GET /Log/auth/statistics?deviceType=...` – returns `{ deviceType, count }` or `{ deviceType, -1 }` on DB error.
- Shared **PostgreSQL** database.
