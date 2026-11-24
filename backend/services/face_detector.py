"""face_detector.py - your original YuNet code as a reusable service.
Model loads once; detection is thread-safe (setInputSize changes shared state)."""
import base64
import threading

import cv2
import numpy as np

from config import Config


class FaceDetectorError(Exception):
    pass


class ModelLoadError(FaceDetectorError):
    pass


class InvalidImageError(FaceDetectorError):
    pass


class FaceDetectorService:
    def __init__(self, model_path=Config.MODEL_PATH, score_threshold=Config.SCORE_THRESHOLD,
                 nms_threshold=Config.NMS_THRESHOLD, top_k=Config.TOP_K):
        self.model_path = model_path
        self.score_threshold = score_threshold
        self.nms_threshold = nms_threshold
        self.top_k = top_k
        self._detector = None
        self._lock = threading.Lock()
        self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            raise ModelLoadError(f"Model file not found: {self.model_path}")
        try:
            self._detector = cv2.FaceDetectorYN.create(
                str(self.model_path), "", (320, 320),
                self.score_threshold, self.nms_threshold, self.top_k)
        except (cv2.error, AttributeError) as exc:
            raise ModelLoadError(f"Could not load YuNet model: {exc}") from exc

    @property
    def is_ready(self):
        return self._detector is not None

    @staticmethod
    def decode_image(data):
        if not data:
            raise InvalidImageError("Empty image data.")
        image = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None or image.size == 0:
            raise InvalidImageError("File is not a valid image.")
        return image

    @staticmethod
    def encode_jpeg(image):
        ok, buf = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, Config.JPEG_QUALITY])
        if not ok:
            raise FaceDetectorError("Failed to encode processed image.")
        return buf.tobytes()

    @staticmethod
    def to_base64_data_url(jpeg_bytes):
        return "data:image/jpeg;base64," + base64.b64encode(jpeg_bytes).decode("ascii")

    def detect(self, image):
        if not self.is_ready:
            raise ModelLoadError("Model is not loaded.")
        if not isinstance(image, np.ndarray) or image.ndim != 3:
            raise InvalidImageError("Image must be a 3-channel color image.")
        height, width = image.shape[:2]
        with self._lock:
            self._detector.setInputSize((width, height))
            _, faces = self._detector.detect(image)
        results = []
        if faces is not None:
            for face in faces:
                x, y, w, h = face[:4].astype(int)
                x, y = max(int(x), 0), max(int(y), 0)
                w, h = min(int(w), width - x), min(int(h), height - y)
                results.append({"x": x, "y": y, "w": w, "h": h,
                                "confidence": round(float(face[14]), 4)})
        return results

    @staticmethod
    def count_faces(faces):
        return len(faces)

    def draw_boxes(self, image, faces, show_count=True):
        out = image.copy()
        for f in faces:
            cv2.rectangle(out, (f["x"], f["y"]), (f["x"] + f["w"], f["y"] + f["h"]),
                          Config.BOX_COLOR, Config.BOX_THICKNESS)
        if show_count:
            cv2.putText(out, f"Total Heads: {len(faces)}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, Config.BOX_COLOR, 2)
        return out

    def process_image_bytes(self, data):
        image = self.decode_image(data)
        faces = self.detect(image)
        processed = self.draw_boxes(image, faces)
        return {"total_faces": len(faces), "faces": faces,
                "image_width": image.shape[1], "image_height": image.shape[0],
                "processed_image": self.to_base64_data_url(self.encode_jpeg(processed))}

    def process_frame_bytes(self, data):
        image = self.decode_image(data)
        faces = self.detect(image)
        return {"total_faces": len(faces), "faces": faces,
                "frame_width": image.shape[1], "frame_height": image.shape[0]}


_instance = None
_instance_lock = threading.Lock()


def get_detector():
    global _instance
    if _instance is None:
        with _instance_lock:
            if _instance is None:
                _instance = FaceDetectorService()
    return _instance
