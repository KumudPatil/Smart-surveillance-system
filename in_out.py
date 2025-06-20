import os 
from datetime import datetime
import cv2

def in_out():
    # Create required directories if they don't exist
    os.makedirs("visitors/in", exist_ok=True)
    os.makedirs("visitors/out", exist_ok=True)

    cap = cv2.VideoCapture(0)

    right, left = "", ""
    x = 300  # Initial x position
    last_logged = None  # To prevent logging the same person multiple times

    while True:
        ret1, frame1 = cap.read()
        ret2, frame2 = cap.read()

        if not (ret1 and ret2):
            print("Camera error.")
            break

        frame1 = cv2.flip(frame1, 1)
        frame2 = cv2.flip(frame2, 1)

        # Get difference and process
        diff = cv2.absdiff(frame2, frame1)
        diff = cv2.blur(diff, (5, 5))
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        if len(contours) > 0:
            max_cnt = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_cnt)

            if w * h > 1500:  # avoid tiny motions
                motion_detected = True
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame1, "MOTION", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

        if motion_detected:
            if right == "" and left == "":
                if x > 500:
                    right = True
                elif x < 200:
                    left = True

            elif right:
                if x < 200 and last_logged != "in":  # Prevent multiple logs for the same person
                    print("Person moved to LEFT (IN)")
                    filename = f"visitors/in/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                    cv2.imwrite(filename, frame1)
                    last_logged = "in"  # Mark as logged in
                    right, left = "", ""

            elif left:
                if x > 500 and last_logged != "out":  # Prevent multiple logs for the same person
                    print("Person moved to RIGHT (OUT)")
                    filename = f"visitors/out/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                    cv2.imwrite(filename, frame1)
                    last_logged = "out"  # Mark as logged out
                    right, left = "", ""

        cv2.imshow("Motion Detection", frame1)

        key = cv2.waitKey(1)
        if key == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the function
if __name__ == "__main__":
    in_out()