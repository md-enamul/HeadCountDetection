# HeadCountDetection - AI Face Detection & Head Count System

Web app that detects and counts faces from a live webcam or uploaded images using OpenCV + the YuNet ONNX model.

## Features
Live webcam detection (browser getUserMedia -> Flask) - image upload detection - bounding boxes and face count - SQLite history (view/delete) - statistics dashboard.

## Tech stack
HTML5, CSS3, JavaScript, Bootstrap 5 | Python, Flask | OpenCV YuNet FaceDetectorYN, NumPy | SQLite

## Installation (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
# place face_detection_yunet_2026may.onnx in backend\models\
python run.py
```
Open http://127.0.0.1:5000

## Folder structure
```
backend/   app.py config.py database.py routes/ services/face_detector.py models/
frontend/  index, dashboard, detection, history, about .html + css/ js/
database/  detection.db (created automatically)
run.py
```

## API
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/detect-image | form-data `image` -> processed image + count (saved) |
| POST | /api/detect-frame | form-data `frame` -> face boxes + count |
| POST | /api/webcam-session | JSON `{"total_faces": n}` -> save session summary |
| GET | /api/history | list records |
| DELETE | /api/history/<id> | delete a record |
| GET | /api/statistics | totals + recent |
| GET | /api/health | backend and model status |

## Screenshots
Add screenshots to `frontend/assets/` and link them here.

## Future scope
Face tracking to avoid double counting, CSV export, user login, multi-camera support, crowd-density analytics.
