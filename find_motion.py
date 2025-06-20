import cv2 
import tkinter as tk
from tkinter import filedialog, simpledialog
import threading
import time
import matplotlib.pyplot as plt
import queue

result_queue = queue.Queue()
human_response_time = 0.20  # Always use this default value

def detect_motion(source, speed=1.0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    local_response_times = []

    while ret:
        motion_start = time.time()

        diff = cv2.absdiff(frame2, frame1)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (5, 5))
        _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            response_time = time.time() - motion_start
            local_response_times.append(response_time)

            x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "MOTION", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        else:
            cv2.putText(frame1, "NO-MOTION", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        cv2.imshow("Motion Detection", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()
        if cv2.waitKey(1) == 27:  # ESC key
            break

        if speed > 1.0:
            time.sleep(max(0.01, 1.0 / (30 * speed)))

    cap.release()
    cv2.destroyAllWindows()

    if local_response_times:
        avg_program_time = sum(local_response_times) / len(local_response_times)
        result_queue.put(avg_program_time)

def noise():
    def run_camera():
        popup.destroy()
        threading.Thread(target=detect_motion, args=(0,), daemon=True).start()
        wait_for_result()

    def run_video():
        file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
        if file:
            speed = simpledialog.askfloat("Speed", "Enter speed (e.g., 1, 2, 3):", minvalue=1.0, maxvalue=5.0)
            popup.destroy()
            threading.Thread(target=detect_motion, args=(file, speed), daemon=True).start()
            wait_for_result()

    def wait_for_result():
        try:
            avg_program_time = result_queue.get_nowait()
            show_average_comparison(avg_program_time)
        except queue.Empty:
            popup.after(100, wait_for_result)

    def show_average_comparison(avg_program_time):
        labels = ['Program', 'Human']
        values = [avg_program_time, human_response_time]

        plt.figure(figsize=(6, 4))
        plt.bar(labels, values, color=['skyblue', 'salmon'])
        plt.ylabel('Average Response Time (seconds)')
        plt.title('Program vs Human Response Time')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    popup = tk.Toplevel()
    tk.Button(popup, text="Live Camera", width=25, height=2, command=run_camera).pack(pady=10)
    tk.Button(popup, text="Upload Video", width=25, height=2, command=run_video).pack(pady=10)