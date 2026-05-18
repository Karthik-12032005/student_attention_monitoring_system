import cv2
import time
import mediapipe as mp
from scipy.spatial import distance
import pyttsx3
from ultralytics import YOLO
from threading import Thread

# -----------------------------
# Voice Setup
# -----------------------------
def _speak_thread(text):
    """Run speech in background thread to avoid blocking main loop"""
    try:
        engine = pyttsx3.init("sapi5")
        engine.setProperty('volume', 1.0)
        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        
        print("Speaking:", text)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking: {e}")

def speak(text):
    """Non-blocking speech function that runs in background thread"""
    thread = Thread(target=_speak_thread, args=(text,), daemon=True)
    thread.start()


def speak_once(text):
    """Speak only if cooldown has elapsed to reduce repeated alerts"""
    global last_speech_time

    if time.time() - last_speech_time >= SPEAK_COOLDOWN:
        speak(text)
        last_speech_time = time.time()

# -----------------------------
# EAR Function
# -----------------------------
def calculate_ear(eye):

    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear

# -----------------------------
# MediaPipe Setup
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

# -----------------------------
# YOLO Model
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# Eye Landmark Indexes
# -----------------------------
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# -----------------------------
# Mouth Landmarks
# -----------------------------
UPPER_LIP = 13
LOWER_LIP = 14

# -----------------------------
# Thresholds
# -----------------------------
EAR_THRESHOLD = 0.27
DROWSY_SECONDS = 3
MOUTH_THRESHOLD = 15
MOUTH_OPEN_SECONDS = 3
HEAD_TURN_SECONDS = 3
SPEAK_COOLDOWN = 3

counter = 0
mouth_open_start = None
drowsy_start = None
head_turn_start = None
pending_head_status = None
last_speech_time = 0

status = "Attentive"
# -----------------------------
# Absence Detection Variables
# -----------------------------
ABSENT_SECONDS = 3

absent_start = None

# -----------------------------
# Main Loop
# -----------------------------
window_name = "Student Attention Monitoring System"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Mirror Effect
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process Face Mesh
    results = face_mesh.process(rgb)

    h, w, _ = frame.shape

    # -----------------------------
    # Phone Detection
    # -----------------------------
    results_yolo = model(frame)

    phone_detected = False

    for result in results_yolo:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])

            class_name = model.names[cls]

            confidence = float(box.conf[0])

            # Detect Cell Phone
            if class_name == "cell phone" and confidence > 0.5:

                phone_detected = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw Box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "Phone Detected",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

    # Voice Alert
    if phone_detected:

        if status != "Using Phone":

            status = "Using Phone"

            speak("Student is using phone")

    # -----------------------------
    # Face Detection
    # -----------------------------
    # -----------------------------
    # No Face Detected
    # -----------------------------
    if not results.multi_face_landmarks:

        if absent_start is None:
            absent_start = time.time()
        elif time.time() - absent_start >= ABSENT_SECONDS:
            if status != "Absent":
                status = "Absent"
                speak_once("Student is absent")

        cv2.putText(
            frame,
            status,
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    else:

        absent_start = None
        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:

                # -----------------------------
                # Eye Points
                # -----------------------------
                left_eye = []
                right_eye = []

                for idx in LEFT_EYE:

                    x = int(face_landmarks.landmark[idx].x * w)
                    y = int(face_landmarks.landmark[idx].y * h)

                    left_eye.append((x, y))

                for idx in RIGHT_EYE:

                    x = int(face_landmarks.landmark[idx].x * w)
                    y = int(face_landmarks.landmark[idx].y * h)

                    right_eye.append((x, y))

                # -----------------------------
                # Calculate EAR
                # -----------------------------
                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)

                avg_ear = (left_ear + right_ear) / 2

                print("EAR:", avg_ear)

                # -----------------------------
                # Draw Eye Points
                # -----------------------------
                for point in left_eye + right_eye:

                    cv2.circle(frame, point, 2, (0, 255, 0), -1)

                # -----------------------------
                # Drowsiness Detection
                # -----------------------------
                if avg_ear < EAR_THRESHOLD:
                    if drowsy_start is None:
                        drowsy_start = time.time()
                    elif time.time() - drowsy_start >= DROWSY_SECONDS:
                        if status != "Drowsy":
                            status = "Drowsy"
                            speak_once("Student is drowsy")
                else:
                    drowsy_start = None
                    if status == "Drowsy":
                        status = "Attentive"
                        speak_once("Student is attentive")

                # -----------------------------
                # Head Direction Detection
                # -----------------------------
                head_status = None

                if status != "Drowsy":

                    nose = face_landmarks.landmark[1]

                    nose_x = int(nose.x * w)

                    center_x = w // 2

                    # More sensitive thresholds
                    LEFT_THRESHOLD = center_x - 60
                    RIGHT_THRESHOLD = center_x + 60

                    if nose_x < LEFT_THRESHOLD:
                        head_status = "Looking Left"
                    elif nose_x > RIGHT_THRESHOLD:
                        head_status = "Looking Right"
                    else:
                        head_status = "Attentive"

                    # Debug values
                    print("Nose X:", nose_x, "Center:", center_x)

                    if head_status in ("Looking Left", "Looking Right"):
                        if pending_head_status != head_status:
                            pending_head_status = head_status
                            head_turn_start = time.time()
                        elif time.time() - head_turn_start >= HEAD_TURN_SECONDS:
                            if status != head_status:
                                status = head_status
                                speak_once(f"Student is {head_status.lower()}")
                    else:
                        pending_head_status = None
                        head_turn_start = None
                        if status != "Attentive":
                            status = "Attentive"
                            speak_once("Student is attentive")

                # -----------------------------
                # Speaking Detection
                # -----------------------------
                upper_lip = face_landmarks.landmark[UPPER_LIP]
                lower_lip = face_landmarks.landmark[LOWER_LIP]

                upper_y = int(upper_lip.y * h)
                lower_y = int(lower_lip.y * h)

                mouth_open = abs(lower_y - upper_y)

                # Draw mouth points
                cv2.circle(
                    frame,
                    (int(upper_lip.x * w), upper_y),
                    3,
                    (255, 0, 0),
                    -1
                )

                cv2.circle(
                    frame,
                    (int(lower_lip.x * w), lower_y),
                    3,
                    (255, 0, 0),
                    -1
                )

                if mouth_open > MOUTH_THRESHOLD:
                    if mouth_open_start is None:
                        mouth_open_start = time.time()
                    elif time.time() - mouth_open_start >= MOUTH_OPEN_SECONDS:
                        if status != "Speaking":
                            status = "Speaking"
                            speak_once("Student is speaking")
                else:
                    mouth_open_start = None

                # -----------------------------
                # Display EAR
                # -----------------------------
                cv2.putText(
                    frame,
                    f"EAR: {avg_ear:.2f}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                # -----------------------------
                # Display Mouth Distance
                # -----------------------------
                cv2.putText(
                    frame,
                    f"Mouth: {mouth_open}",
                    (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2
                )

                # -----------------------------
                # Display Status
                # -----------------------------
                cv2.putText(
                    frame,
                    status,
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

    # -----------------------------
    # Show Output
    # -----------------------------
    cv2.imshow(window_name, frame)

    # ESC Key or 'q' to exit
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()