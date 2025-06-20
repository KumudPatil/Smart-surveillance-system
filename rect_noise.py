import cv2
import numpy as np
from twilio.rest import Client

def detect_weapon(source=0):
    
    account_sid = 'ACca5e145d3b6570a3125f8bfec0c2fd38'
    auth_token = '25f2237337bfc1a0087c61882548ed3a'
    twilio_phone_number = '+1 620 490 3424'
    destination_phone_number = '+919307773031'

    def send_sms_alert():
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="⚠️ Alert: Weapon detected by surveillance system!",
            from_=twilio_phone_number,
            to=destination_phone_number
        )
        print(f"SMS sent: {message.sid}")

    net = cv2.dnn.readNet("yolov3_training_2000.weights", "yolov3_testing.cfg")
    classes = ["Weapon"]
    output_layer_names = net.getUnconnectedOutLayersNames()
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    sms_sent = False

    while True:
        ret, img = cap.read()
        if not ret:
            break

        height, width, _ = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layer_names)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            print("Weapon detected!")
            if not sms_sent:
                send_sms_alert()
                sms_sent = True
        else:
            sms_sent = False

        cv2.imshow("Weapon Detection", img)
        if cv2.waitKey(1) == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()


def show_weapon_popup():
    import tkinter as tk
    from tkinter import filedialog
    import threading

    def start_live_camera():
        popup.destroy()
        threading.Thread(target=detect_weapon, args=(0,), daemon=True).start()

    def start_video_file():
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
        )
        if file_path:
            popup.destroy()
            threading.Thread(target=detect_weapon, args=(file_path,), daemon=True).start()

    popup = tk.Toplevel()
    popup.title("Select Input Source")
    popup.geometry("300x150")
    popup.resizable(False, False)

    label = tk.Label(popup, text="Choose Input for Weapon Detection", font=("Arial", 11))
    label.pack(pady=15)

    btn_live = tk.Button(popup, text="1️⃣ Live Camera", width=20, command=start_live_camera)
    btn_live.pack(pady=5)

    btn_video = tk.Button(popup, text="2️⃣ Upload Video", width=20, command=start_video_file)
    btn_video.pack(pady=5)


