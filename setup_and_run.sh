#!/usr/bin/env bash
# One-click setup + run for Mac/Linux.
cd "$(dirname "$0")"
[ -d venv ] || python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
python manage.py migrate
python manage.py runstreamlit
