# ================= SET TWILIO ENV VARIABLES (GUARANTEED FIX) =================
import os

# Twilio credentials should be set as environment variables
# Example (DO NOT hardcode):
# export TWILIO_SID=your_sid
# export TWILIO_TOKEN=your_token

# ============================================================================

import cv2
import mediapipe as mp
import numpy as np
import json
import random
import sys
from datetime import datetime

from drowsiness import (
    eye_aspect_ratio,
    mouth_open_ratio,
    extract_eye_mouth_coords,
    head_tilt_angle
)

from alert import (
    play_sound_alert,
    display_warning,
    bfs_alert_propagation,
    generate_gen_ai_alert,
    speak_gen_ai_alert,
    send_whatsapp_alert
)

from vehicle_routing import bfs_vehicle_route

print("✅ main.py started")

# ================= PARAMETERS =================
EAR_THRESH = 0.23
EAR_CONSEC_FRAMES = 20
MOUTH_THRESH = 0.6
YAWN_CONSEC_FRAMES = 20
ALERT_SOUND = "assets/alert.wav"

# ================= ALERT TREE =================
ALERT_TREE = {
    "Driver": ["Co-driver"],
    "Co-driver": ["Emergency Contact"],
    "Emergency Contact": ["Vehicle System"],
    "Vehicle System": []
}

# ================= CAMERA INIT =================
cap = None
for i in [0, 1, 2]:
    cam = cv2.VideoCapture(i)
    if cam.isOpened():
        cap = cam
        print(f"✅ Camera opened at index {i}")
        break

if cap is None:
    print("❌ ERROR: No webcam detected")
    sys.exit(1)

print("Camera FPS:", cap.get(cv2.CAP_PROP_FPS))

# ================= DASHBOARD INIT =================
try:
    with open("dashboard_data.json", "r") as f:
        data = json.load(f)
except Exception:
    data = {}

data.setdefault("event_log", [])
data.setdefault("history", [])

with open("dashboard_data.json", "w") as f:
    json.dump(data, f, indent=2)


def update_dashboard(grid, path, alert_order, message):
    with open("dashboard_data.json", "r") as f:
        data = json.load(f)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = f"{timestamp}: {message}"

    data["grid"] = grid
    data["path"] = path
    data["alert_order"] = alert_order
    data["event_log"].append(event)
    data["event_log"] = data["event_log"][-20:]
    data["history"].append(event)

    with open("dashboard_data.json", "w") as f:
        json.dump(data, f, indent=2)


def generate_random_grid(rows=5, cols=6, obstacle_prob=0.3):
    return [
        [1 if random.random() < obstacle_prob else 0 for _ in range(cols)]
        for _ in range(rows)
    ]


def random_open_cell(grid):
    cells = [
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[0]))
        if grid[r][c] == 0
    ]
    return random.choice(cells)


# ================= MAIN LOOP =================
COUNTER = 0
YAWN_COUNTER = 0
ALARM_ON = False
YAWN_ALARM_ON = False

mp_face_mesh = mp.solutions.face_mesh

with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            left_eye, right_eye, mouth = extract_eye_mouth_coords(
                landmarks, frame.shape
            )

            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2
            mouth_ratio = mouth_open_ratio(mouth)

            # ================= DROWSINESS =================
            if ear < EAR_THRESH:
                COUNTER += 1
                if COUNTER >= EAR_CONSEC_FRAMES and not ALARM_ON:
                    ALARM_ON = True

                    play_sound_alert(ALERT_SOUND)
                    display_warning(frame)

                    grid = generate_random_grid()
                    start = random_open_cell(grid)
                    stop = random_open_cell(grid)
                    while stop == start:
                        stop = random_open_cell(grid)

                    path = bfs_vehicle_route(grid, start, stop)
                    order = bfs_alert_propagation(ALERT_TREE, "Driver")

                    if path:
                        alert_count = len(data.get("history", []))

                        ai_message = generate_gen_ai_alert(
                            "Drowsiness", alert_count
                        )

                        speak_gen_ai_alert(ai_message)

                        # 📲 WhatsApp alert (TEST MODE: send on first alert)
                        if alert_count >= 1:
                            send_whatsapp_alert(ai_message)

                        update_dashboard(grid, path, order, ai_message)
            else:
                COUNTER = 0
                ALARM_ON = False

            # ================= YAWNING =================
            if mouth_ratio > MOUTH_THRESH:
                YAWN_COUNTER += 1
                if YAWN_COUNTER >= YAWN_CONSEC_FRAMES and not YAWN_ALARM_ON:
                    YAWN_ALARM_ON = True

                    play_sound_alert(ALERT_SOUND)
                    display_warning(frame, "YAWNING DETECTED!")

                    grid = generate_random_grid()
                    start = random_open_cell(grid)
                    stop = random_open_cell(grid)
                    while stop == start:
                        stop = random_open_cell(grid)

                    path = bfs_vehicle_route(grid, start, stop)
                    order = bfs_alert_propagation(ALERT_TREE, "Driver")

                    if path:
                        alert_count = len(data.get("history", []))

                        ai_message = generate_gen_ai_alert(
                            "Yawning", alert_count
                        )

                        speak_gen_ai_alert(ai_message)

                        # 📲 WhatsApp alert (TEST MODE)
                        if alert_count >= 1:
                            send_whatsapp_alert(ai_message)

                        update_dashboard(grid, path, order, ai_message)
            else:
                YAWN_COUNTER = 0
                YAWN_ALARM_ON = False

        cv2.imshow("Drowsiness Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
print("✅ Program exited cleanly")
