import os 
import cv2
import numpy as np
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox, simpledialog
import face_recognition

# Ensure 'persons' directory exists
if not os.path.exists('persons'):
    os.makedirs('persons')

# Collect face data
def collect_data():
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Input", "Enter name of person:")

    if not name:
        messagebox.showerror("Input Error", "Name cannot be empty.")
        return

    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), encoding in zip(face_locations, encodings):
            count += 1
            filename = f"persons/{name}-{count}.npy"
            np.save(filename, encoding)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{count}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Capturing Faces", frame)

        if cv2.waitKey(1) == 27 or count >= 10:  # ESC or 10 samples
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Captured {count} images for {name}.")

# Identify person
def identify():
    known_encodings = []
    known_names = []

    for file in os.listdir("persons"):
        if file.endswith(".npy"):
            path = os.path.join("persons", file)
            encoding = np.load(path)
            name = file.split('-')[0]
            known_encodings.append(encoding)
            known_names.append(name)

    if not known_encodings:
        messagebox.showerror("Error", "No face data found. Please add members first.")
        return

    cap = cv2.VideoCapture(0)
    threshold = 0.45  # adjust as needed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), encoding in zip(face_locations, encodings):
            distances = face_recognition.face_distance(known_encodings, encoding)
            min_distance = np.min(distances) if len(distances) > 0 else None

            if min_distance is not None and min_distance < threshold:
                match_index = np.argmin(distances)
                name = known_names[match_index]
                label = f"{name} ({min_distance:.2f})"
                color = (0, 255, 0)
            else:
                label = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Identify Member", frame)

        if cv2.waitKey(1) == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# GUI
def maincall():
    root = tk.Tk()
    root.geometry("500x180")
    root.title("Smart CCTV - Face Recognition")

    label = tk.Label(root, text="Smart CCTV Face Recognition", font=("Helvetica", 20, "bold"))
    label.pack(pady=(10, 5))

    btn_font = font.Font(size=14)

    btn_add = tk.Button(root, text="Add Member", command=collect_data, font=btn_font, width=20, height=2)
    btn_add.pack(pady=10)

    btn_identify = tk.Button(root, text="Identify Member", command=identify, font=btn_font, width=20, height=2)
    btn_identify.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    maincall()