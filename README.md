# Auth API — Django + Custom JWT + Redis

## Quick Start

```bash
# Copy environment variables
cp env.example .env
cp env.example .env.docker

# Build and run containers
make build && make down && make up
```

---

## Project Initialization

```bash
# Apply database migrations
make migrate

# Load fixtures
make load_fixtures
```

## Roles & Test Users

- `USER` — default role  
- `ADMIN` — elevated access  
- Controlled with custom `permissions` classes

### Test Users:

| Role   | Email            | Password |
|--------|------------------|----------|
| Admin  | root@mail.com    | root     |
| User   | user@example.com | 12345678 |

---

## Docker Services

| Service | Purpose              |
|---------|----------------------|
| `web`   | Django + uv          |
| `db`    | PostgreSQL database  |
| `redis` | Redis for token state|

---

## Tech Stack

- Python 3.12
- Django + DRF
- PostgreSQL
- Redis
- uvicorn
- uv (package manager)
