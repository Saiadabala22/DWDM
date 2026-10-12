#!/usr/bin/env python
"""Project-root manage.py. Run it from this folder:

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver          # Django API + admin  -> http://127.0.0.1:8000
    python manage.py runstreamlit       # Streamlit app       -> http://localhost:8501
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DJANGO_DIR = ROOT / "backend" / "django_backend"


def main():
    sys.path.insert(0, str(DJANGO_DIR))
    sys.path.insert(0, str(ROOT))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dwdm_backend.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
