#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py collectstatic --noinput --settings=tours_travels.settings_prod
python3 manage.py migrate --settings=tours_travels.settings_prod
python3 manage.py createcachetable --settings=tours_travels.settings_prod