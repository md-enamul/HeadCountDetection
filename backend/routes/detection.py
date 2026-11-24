"""detection.py - /api/detect-image, /api/detect-frame, /api/webcam-session"""
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from config import Config
from database import add_record
from services.face_detector import FaceDetectorError, InvalidImageError, get_detector

bp = Blueprint("detection", __name__)


def fail(msg, code=400):
    return jsonify(success=False, error=msg), code


@bp.post("/api/detect-image")
def detect_image():
    f = request.files.get("image")
    if f is None or not f.filename:
        return fail("No image uploaded.")
    name = secure_filename(f.filename)
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in Config.ALLOWED_EXTENSIONS:
        return fail("Unsupported file type. Use JPG, PNG, BMP or WEBP.")
    try:
        result = get_detector().process_image_bytes(f.read())  # in memory: no temp files
    except InvalidImageError as e:
        return fail(str(e))
    except FaceDetectorError as e:
        return fail(str(e), 500)
    result["id"] = add_record("image", result["total_faces"], name)
    result["filename"] = name
    return jsonify(success=True, **result)


@bp.post("/api/detect-frame")
def detect_frame():
    f = request.files.get("frame")
    if f is None:
        return fail("No frame received.")
    try:
        result = get_detector().process_frame_bytes(f.read())
    except InvalidImageError as e:
        return fail(str(e))
    except FaceDetectorError as e:
        return fail(str(e), 500)
    return jsonify(success=True, **result)


@bp.post("/api/webcam-session")
def webcam_session():
    total = (request.get_json(silent=True) or {}).get("total_faces")
    if not isinstance(total, int) or isinstance(total, bool) or not 0 <= total <= 1000:
        return fail("total_faces must be an integer between 0 and 1000.")
    return jsonify(success=True, id=add_record("webcam", total))
