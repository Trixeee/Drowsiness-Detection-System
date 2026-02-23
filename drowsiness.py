import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial import distance as dist

mp_face_mesh = mp.solutions.face_mesh

# Indices for left and right eyes and mouth (Mediapipe Face Mesh)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14, 78, 308]

# EAR calculation
def eye_aspect_ratio(eye_points):
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    C = dist.euclidean(eye_points[0], eye_points[3])
    return (A + B) / (2.0 * C)

# Yawn detection (distance between upper and lower lip)
def mouth_open_ratio(mouth_points):
    A = dist.euclidean(mouth_points[0], mouth_points[1])  # vertical
    B = dist.euclidean(mouth_points[2], mouth_points[3])  # horizontal
    return A / B

# Head pose estimation (simple: vertical movement of nose tip)
def get_head_pose(landmarks, image_shape):
    # Use nose tip and chin for simple up/down estimation
    nose_tip = np.array(landmarks[1])
    chin = np.array(landmarks[152])
    return nose_tip, chin

# Extract eye and mouth coordinates from landmarks
def extract_eye_mouth_coords(landmarks, image_shape):
    h, w = image_shape[:2]
    left_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in LEFT_EYE]
    right_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in RIGHT_EYE]
    mouth = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in MOUTH]
    return left_eye, right_eye, mouth

# Head tilt angle calculation (pitch)
def head_tilt_angle(landmarks, image_shape):
    h, w = image_shape[:2]
    nose = landmarks[1]
    chin = landmarks[152]
    x1, y1 = int(nose.x * w), int(nose.y * h)
    x2, y2 = int(chin.x * w), int(chin.y * h)
    # Calculate angle between vertical and nose-chin line
    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    return abs(angle) 