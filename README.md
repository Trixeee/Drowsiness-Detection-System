# Drowsiness Detection System

## Overview
Detects drowsiness in real-time using a webcam by analyzing eye closure and yawning. Triggers alerts and simulates smart responses using BFS algorithms. Features a modern web dashboard for live visualization of vehicle routing, alert propagation, and event history.

## Features

- Real-time face, eye, and mouth detection using webcam
- Eye Aspect Ratio (EAR) based drowsiness detection
- Yawning detection
- On-screen visual warnings
- Sound alerts
- Voice-based AI alerts
- WhatsApp alert notifications (Twilio)
- Live event logging
- Modern Flask-based dashboard
- Secure handling of credentials using environment variables

## Setup
1. Clone the repository or download the project files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install flask
   ```
3. Ensure you have a webcam connected.

## Usage
### 1. Start the Detection System
```bash
python main.py
```
### 2. Start the Web Dashboard
```bash
python app.py
```
### 3. Open the Dashboard
Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

- The dashboard will update live as events are detected.
- The event log shows only current session events; history shows all past activities (can be cleared).
- The grid, path, and alert propagation tree are shown both on the dashboard and in the terminal.

## Project Structure
- `main.py` — Main entry point (detection, alerting, dashboard updates)
- `drowsiness.py` — Drowsiness detection logic
- `alert.py` — Alert system and BFS alert propagation
- `app.py` — Flask web dashboard backend
- `templates/dashboard.html` — Dashboard frontend
- `dashboard_data.json` — Shared data for dashboard and detection
- `assets/alert.wav` — Alert sound

## Notes
- All processing is done locally for privacy.
- BFS-based features are simulated for demonstration.
- The dashboard is fully responsive and visually enhanced for a modern look.

## 🔐 Security Note

This project follows best practices for handling sensitive credentials.

- No API keys or secrets are hard-coded in the source code
- Twilio credentials are loaded using environment variables
- A `.env.example` file is provided as a reference
- The actual `.env` file should never be committed to version control

This approach ensures security, prevents credential leaks, and aligns with real-world industry standards.


## 🧠 How It Works

1. Webcam captures live video frames
2. Mediapipe Face Mesh extracts facial landmarks
3. Eye Aspect Ratio (EAR) detects prolonged eye closure
4. Mouth ratio detects yawning behavior
5. Alerts are triggered after consecutive frames
6. Alerts are delivered via:
   - On-screen warning
   - Sound alert
   - Voice alert
   - WhatsApp notification
7. All events are logged and visualized on a web dashboard
--- 
