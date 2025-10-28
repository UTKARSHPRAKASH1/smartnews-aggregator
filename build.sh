#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install all packages
pip install -r requirements.txt

# 2. Collect all static files (CSS, JS) into one folder
python manage.py collectstatic --no-input

# 3. Run database migrations to build the tables
python manage.py migrate
