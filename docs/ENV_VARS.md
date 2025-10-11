# Environment variables

These variables control runtime behavior for storage, API host/port, and database configuration.

## Storage selection

- HBNB_TYPE_STORAGE: `file` (default) or `db`

## API

- HBNB_API_HOST: Host for the API app (default: `0.0.0.0`)
- HBNB_API_PORT: Port for the API app (default: `5000`)

## Database (used when HBNB_TYPE_STORAGE=db)

- HBNB_MYSQL_USER: MySQL username
- HBNB_MYSQL_PWD: MySQL password
- HBNB_MYSQL_HOST: MySQL host (e.g., `127.0.0.1`)
- HBNB_MYSQL_DB: Database name (e.g., `hbnb_dev_db`)
- HBNB_ENV: `dev` or `test` (drops all tables on init when set to `test`)
