@echo off
REM One-click setup + run for Windows. Double-click or run from the project folder.
cd /d "%~dp0"
if not exist venv (python -m venv venv)
call venv\Scripts\activate
python -m pip install -q -r requirements.txt
python manage.py migrate
echo.
echo Starting Streamlit app at http://localhost:8501  (Ctrl+C to stop)
python manage.py runstreamlit
