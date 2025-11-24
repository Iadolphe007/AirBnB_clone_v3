# AirBnB Clone v3 API

Flask application exposing a REST API mounted at `/api/v1` via a Blueprint (`app_views`).

## Run

```bash
export HBNB_API_HOST=0.0.0.0
export HBNB_API_PORT=5000
# Storage backend (default: file)
export HBNB_TYPE_STORAGE=file  # or db
python3 -m api.v1.app
```

> [!NOTE]
> When using DB storage, also set: `HBNB_MYSQL_USER`, `HBNB_MYSQL_PWD`, `HBNB_MYSQL_HOST`, `HBNB_MYSQL_DB`. See `../docs/ENV_VARS.md`.

## Key endpoints

- GET `/api/v1/status` → `{ "status": "OK" }`
- GET `/api/v1/stats` → counts per model
- CRUD:
  - `/api/v1/states`
  - `/api/v1/cities`
  - `/api/v1/amenities`
  - `/api/v1/users`
  - `/api/v1/places`
  - `/api/v1/reviews`
  - `/api/v1/places/<place_id>/amenities`

CORS is enabled for `/api/*` with origin `0.0.0.0` in `v1/app.py`.

## Health check

```bash
curl -s http://127.0.0.1:5000/api/v1/status | jq .
curl -s http://127.0.0.1:5000/api/v1/stats | jq .
```
