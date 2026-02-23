# Drowsiness Detection System

## Overview
Detects drowsiness in real-time using a webcam by analyzing eye closure and yawning. Triggers alerts and simulates smart responses using BFS algorithms. Features a modern web dashboard for live visualization of vehicle routing, alert propagation, and event history.

## Features
- Real-time face, eye, and mouth detection (Mediapipe + OpenCV)
- Eye Aspect Ratio (EAR) for drowsiness detection
- Yawn detection
- On-screen and sound alerts
- BFS-based alert propagation (simulated)
- BFS-based vehicle routing to safe stop (simulated)
- **Modern web dashboard**:
  - Live grid and path visualization (with start, end, obstacles, and route)
  - Alert propagation tree
  - Event log (current session)
  - History of all past activities (with delete option)
  - Responsive, visually appealing design

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
- `vehicle_routing.py` — BFS vehicle routing simulation
- `app.py` — Flask web dashboard backend
- `templates/dashboard.html` — Dashboard frontend
- `dashboard_data.json` — Shared data for dashboard and detection
- `assets/alert.wav` — Alert sound

## Notes
- All processing is done locally for privacy.
- BFS-based features are simulated for demonstration.
- The dashboard is fully responsive and visually enhanced for a modern look.

--- 