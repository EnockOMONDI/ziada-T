#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput --settings=tours_travels.settings_prod
python manage.py migrate --settings=tours_travels.settings_prod
python manage.py createcachetable --settings=tours_travels.settings_prod
