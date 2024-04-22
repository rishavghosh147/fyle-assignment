#!/bin/bash

# to stop on first error
set -e

#prevent to generate pycache files
export PYTHONDONTWRITEBYTECODE='1'

# Delete older .pyc files
# find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Run required migrations
export FLASK_APP=core/server.py

#Remove previous database
# rm core/store.sqlite3

# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
flask db upgrade -d core/migrations/

# Run server
gunicorn -c gunicorn_config.py core.server:app
