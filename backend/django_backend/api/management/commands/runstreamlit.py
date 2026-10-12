import subprocess
import sys
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Start the Streamlit frontend (frontend/app.py)."

    def add_arguments(self, parser):
        parser.add_argument("--port", default="8501")

    def handle(self, *args, **opts):
        root = Path(__file__).resolve().parents[5]
        app = root / "frontend" / "app.py"
        self.stdout.write(self.style.SUCCESS(f"Starting Streamlit on http://localhost:{opts['port']}"))
        subprocess.call([sys.executable, "-m", "streamlit", "run", str(app), "--server.port", opts["port"]], cwd=root)
