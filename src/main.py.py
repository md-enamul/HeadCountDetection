
import cv2

camera = cv2.VideoCapture(0)

detector = cv2.FaceDetectorYN.create(
    r"C:\Users\mdena\Desktop\HeadCountDetection\src\face_detection_yunet_2026may.onnx",
    "",
    (320, 320),
    0.7,
    0.3,
    5000
)

while True:
    ret, frame = camera.read()
    if not ret:
        print("Camera not working")
        break

    h, w = frame.shape[:2]
    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)
    count = 0 if faces is None else len(faces)

    if faces is not None:
        for face in faces:
            x, y, fw, fh = face[:4].astype(int)
            cv2.rectangle(frame, (x, y), (x+fw, y+fh), (0,255,0), 2)

    cv2.putText(frame, f"Head Count: {count}",
                (10, 35), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 0), 2)

    cv2.imshow("Head Count Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
