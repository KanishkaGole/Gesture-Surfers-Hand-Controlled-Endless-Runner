import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from collections import deque
import threading
import os

class HandTracker:
    def __init__(self):
        # Use MediaPipe Tasks API (Modern & compatible with Python 3.13)
        model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            running_mode=vision.RunningMode.IMAGE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        self.current_gesture = None
        self.running = True
        self.cap = None
        
        # Buffer for swipe detection
        self.wrist_history = deque(maxlen=10)

    def start(self):
        self.cap = cv2.VideoCapture(0)
        threading.Thread(target=self._update, daemon=True).start()

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def _update(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            # Convert to MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # Detect
            results = self.detector.detect(mp_image)

            gesture = "IDLE"
            if results.hand_landmarks:
                # results.hand_landmarks is a list of lists of landmarks
                hand_lms = results.hand_landmarks[0]
                gesture = self._classify_gesture(hand_lms)
                # Annotate skeleton
                self._draw_skeleton(frame, hand_lms)
            else:
                self.wrist_history.clear()
            
            # Debug view
            color = (0, 255, 0) if gesture != "IDLE" else (0, 0, 255)
            cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.imshow("Camera Feed - Gesture Surfers", frame)
            
            self.current_gesture = gesture
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def _draw_skeleton(self, frame, landmarks):
        h, w, _ = frame.shape
        # Define connections (pairs of landmark indices)
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4), # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8), # Index
            (0, 9), (9, 10), (10, 11), (11, 12), # Middle
            (0, 13), (13, 14), (14, 15), (15, 16), # Ring
            (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
            (5, 9), (9, 13), (13, 17) # Palm
        ]
        
        # Convert normalized coordinates to pixel coordinates
        points = []
        for lm in landmarks:
            points.append((int(lm.x * w), int(lm.y * h)))
            
        # Draw lines
        for start_idx, end_idx in connections:
            cv2.line(frame, points[start_idx], points[end_idx], (0, 255, 255), 2)
            
        # Draw points
        for pt in points:
            cv2.circle(frame, pt, 4, (255, 0, 100), -1)

    def _classify_gesture(self, landmarks):
        lms = landmarks
        
        # Count fingers (Index, Middle, Ring, Pinky)
        fingers_up = []
        for tip, mcp in [(8, 5), (12, 9), (16, 13), (20, 17)]:
            fingers_up.append(lms[tip].y < lms[mcp].y)
        
        count = sum(fingers_up)
        
        # Gesture Mapping
        if count == 0:
            return "SLIDE"
        elif count == 1:
            return "LANE_0"
        elif count == 2:
            return "LANE_1"
        elif count == 3:
            return "LANE_2"
        elif count >= 4:
            return "JUMP"

        return "IDLE"

    def get_gesture(self):
        # We don't reset LANE gestures because they are absolute states
        g = self.current_gesture
        if g in ["JUMP", "SLIDE"]:
            self.current_gesture = "IDLE"
        return g
