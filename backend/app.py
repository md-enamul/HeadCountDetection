"""app.py - Flask application factory. Serves the API and the frontend."""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import database
from config import Config
from routes import detection, history, statistics
from services.face_detector import FaceDetectorError, get_detector


def create_app():
    app = Flask(__name__, static_folder=str(Config.FRONTEND_FOLDER), static_url_path="")
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH
    CORS(app)
    Config.UPLOAD_FOLDER.mkdir(exist_ok=True)
    database.init_db()

    try:
        get_detector()
        print("[OK] YuNet model loaded")
    except FaceDetectorError as e:
        print("[ERROR]", e)

    for module in (detection, history, statistics):
        app.register_blueprint(module.bp)

    @app.get("/")
    def home():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/api/health")
    def health():
        try:
            ok = get_detector().is_ready
            err = None
        except FaceDetectorError as e:
            ok, err = False, str(e)
        return jsonify(success=True, status="ok" if ok else "degraded",
                       model_loaded=ok, model_file=Config.MODEL_PATH.name, error=err)

    @app.errorhandler(413)
    def too_large(_):
        return jsonify(success=False, error="File too large (max 10 MB)."), 413

    @app.errorhandler(404)
    def not_found(_):
        if request.path.startswith("/api/"):
            return jsonify(success=False, error="Endpoint not found."), 404
        return "Page not found", 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify(success=False, error="Internal server error."), 500

    return app
