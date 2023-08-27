#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USERNAME" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER docker;
	CREATE DATABASE bot_db;
	GRANT ALL PRIVILEGES ON DATABASE bot_db TO docker;
EOSQL