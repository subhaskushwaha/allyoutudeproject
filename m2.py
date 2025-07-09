import cv2
import mediapipe as mp
import numpy as np
import os

# Load image paths
image_folder = 'images'
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.jpg')])
image_index = 0

# Function to load and resize current image
def get_current_image():
    img = cv2.imread(os.path.join(image_folder, image_files[image_index]))
    return cv2.resize(img, (400, 300))

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = None
swipe_cooldown = 20
cooldown_counter = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Draw current image at corner
    overlay_img = get_current_image()
    frame[50:350, 50:450] = overlay_img

    if cooldown_counter > 0:
        cooldown_counter -= 1

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_x = int(index_tip.x * w)

            # Detect swipe
            if prev_x is not None and cooldown_counter == 0:
                delta = index_x - prev_x
                if delta > 50:
                    image_index = max(0, image_index - 1)  # swipe right → previous
                    cooldown_counter = swipe_cooldown
                elif delta < -50:
                    image_index = min(len(image_files) - 1, image_index + 1)  # swipe left → next
                    cooldown_counter = swipe_cooldown

            prev_x = index_x

    cv2.putText(frame, f"Image: {image_index + 1}/{len(image_files)}", (50, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Gesture-Based Slideshow", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
