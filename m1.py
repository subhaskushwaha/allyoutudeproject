import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# Set reference hand area (e.g., fixed area on screen)
ref_x, ref_y = 200, 150  # Top-left corner
ref_w, ref_h = 200, 300  # Width & height

# Flag to start UI after hand detected
start_effect = False

def draw_reference_hand(frame):
    # Draw a translucent box as reference hand position
    overlay = frame.copy()
    cv2.rectangle(overlay, (ref_x, ref_y), (ref_x + ref_w, ref_y + ref_h), (0, 255, 255), -1)
    alpha = 0.3  # Transparency factor
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, "Place Hand Here", (ref_x, ref_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

def hand_in_reference_area(landmarks, img_w, img_h):
    for lm in landmarks.landmark:
        x = int(lm.x * img_w)
        y = int(lm.y * img_h)
        if not (ref_x < x < ref_x + ref_w and ref_y < y < ref_y + ref_h):
            return False
    return True

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        start_effect = True  # Start everything once hand is detected

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if start_effect:
                draw_reference_hand(frame)

                # Check if hand is inside the reference area
                if hand_in_reference_area(hand_landmarks, w, h):
                    # Draw lighting effect
                    cv2.circle(frame, (ref_x + ref_w//2, ref_y + ref_h//2), 120, (0, 255, 0), thickness=20)
                    cv2.putText(frame, "IRAM Man Power Open", (100, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 4)

    cv2.imshow('Hand Scan Activation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
