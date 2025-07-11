import cv2
import mediapipe as mp

handsModule = mp.solutions.hands

mod = handsModule.Hands()

def count_hands(frame):
    results = mod.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        return len(results.multi_hand_landmarks)
    else:
        return 0
# Example of how to use this function:

# while True:
#     ret, frame = cap.read()
#     hand_count = count_hands(frame)
#     print("Number of hands detected:", hand_count)
#     cv2.imshow('Hand Detection', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()