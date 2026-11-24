"""config.py - central settings used by every backend module."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    MODEL_PATH = BASE_DIR / "backend" / "models" / "face_detection_yunet_2026may.onnx"
    DATABASE_PATH = BASE_DIR / "database" / "detection.db"
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    FRONTEND_FOLDER = BASE_DIR / "frontend"

    # YuNet settings (0.9 = OpenCV default your original code used)
    SCORE_THRESHOLD = 0.9
    NMS_THRESHOLD = 0.3
    TOP_K = 5000

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp"}
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    BOX_COLOR = (0, 255, 0)
    BOX_THICKNESS = 2
    JPEG_QUALITY = 90

    HOST = "127.0.0.1"
    PORT = 5000
