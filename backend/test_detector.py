"""Run from /backend:  python test_detector.py [optional_image_path]"""
import sys
import cv2
from services.face_detector import FaceDetectorError, InvalidImageError, ModelLoadError, get_detector

try:
    d = get_detector()
    print("[PASS] model loaded")
except ModelLoadError as e:
    sys.exit(f"[FAIL] {e}")
try:
    d.process_image_bytes(b"not an image")
    print("[FAIL] invalid image accepted")
except InvalidImageError:
    print("[PASS] invalid image rejected")
if len(sys.argv) > 1:
    img = cv2.imread(sys.argv[1])
else:
    cam = cv2.VideoCapture(0); ok, img = cam.read(); cam.release()
    img = img if ok else None
if img is None:
    sys.exit("[FAIL] no image/webcam frame")
faces = d.detect(img)
print(f"[PASS] faces found: {len(faces)}")
cv2.imwrite("test_output.jpg", d.draw_boxes(img, faces))
