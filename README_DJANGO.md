# DWDM Integrated System - Django + SQLite

## Structure

frontend/
    app.py
    pages/
    assets/
    utils/

backend/
    django_backend/
        manage.py
        dwdm_backend/
            settings.py
            urls.py
            asgi.py
            wsgi.py
        api/
            models.py
            serializers.py
            views.py
            urls.py
            admin.py
    data_input/
    preprocessing/
    etl/
    database/
    olap/
    classification/
    association_mining/
    clustering/
    evaluation/
    visualization/
    final_report/

## Setup

1. No database server needed: SQLite files are created in `data/` automatically.

2. Optional: copy `.env.example` to `.env` to change settings.

3. Install:
   pip install -r requirements.txt

4. Start Django:
   cd backend/django_backend
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver 8000

5. JWT:
   POST /api/token/
   POST /api/token/refresh/

6. API endpoints:
   /api/datasets/
   /api/analysis-runs/
   /admin/

7. Start Streamlit frontend from the project root:
   streamlit run frontend/app.py

The Django backend is the API layer; SQLite is the persistent database (data/django.sqlite3 for Django, data/dwdm_warehouse.db for the warehouse).
