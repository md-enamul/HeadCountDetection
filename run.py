"""Start the app:  python run.py   then open http://127.0.0.1:5000"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

from app import create_app  # noqa: E402
from config import Config  # noqa: E402

app = create_app()

if __name__ == "__main__":
    print(f"Open http://{Config.HOST}:{Config.PORT} in your browser")
    app.run(host=Config.HOST, port=Config.PORT, debug=False, threaded=True)
