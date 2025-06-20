import cv2
import os
from datetime import datetime

# Ensure the 'recordings' directory exists
if not os.path.exists('recordings'):
    os.makedirs('recordings')

def record():
    cap = cv2.VideoCapture(0)

    # Check if the video capture is successful
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'recordings/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.avi', fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Adding timestamp to each frame
        cv2.putText(frame, f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

        # Write the frame to the video file
        out.write(frame)

        # Display the video stream
        cv2.imshow("Press ESC to stop", frame)

        # Check if the ESC key is pressed to stop recording
        if cv2.waitKey(1) == 27:
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            break