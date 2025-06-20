 import tkinter as tk
import tkinter.font as font
from in_out import in_out
from motion import noise
from record import record
from PIL import Image, ImageTk
from find_motion import find_motion
from identify import maincall
from weapon_detection import show_weapon_popup
import threading

window = tk.Tk()
window.title("Smart CCTV")
window.iconphoto(False, tk.PhotoImage(file='mn.png'))
window.geometry('1080x700')

frame1 = tk.Frame(window)
frame1.pack(pady=20)

label_title = tk.Label(frame1, text="Smart CCTV Camera")
label_font = font.Font(size=35, weight='bold', family='Helvetica')
label_title['font'] = label_font
label_title.grid(row=0, column=0, columnspan=3, pady=(10, 20))

# ---------- Load & Resize Icons ---------- #
def load_icon(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

icon = load_icon('icons/spy.png', (150, 150))
label_icon = tk.Label(frame1, image=icon)
label_icon.grid(row=1, column=1, pady=10)

btn1_image = load_icon('icons/lamp.png', (50, 50))
btn2_image = load_icon('icons/rectangle-of-cutted-line-geometrical-shape.png', (50, 50))
btn3_image = load_icon('icons/security-camera.png', (50, 50))
btn4_image = load_icon('icons/recording.png', (50, 50))
btn5_image = load_icon('icons/exit.png', (50, 50))
btn6_image = load_icon('icons/incognito.png', (50, 50))
btn7_image = load_icon('icons/recording.png', (50, 50))

btn_font = font.Font(size=20)

# ---------- Button Commands ---------- #
def run_weapon_popup():
    threading.Thread(target=show_weapon_popup, daemon=True).start()

# ---------- Buttons Layout (3x3 grid) ---------- #
btn1 = tk.Button(frame1, text='Monitor', height=100, width=200, fg='green',
                 command=find_motion, image=btn1_image, compound='left', font=btn_font)
btn1.grid(row=2, column=0, padx=20, pady=20)

btn2 = tk.Button(frame1, text='Rectangle', height=100, width=200, fg='orange',
                 command=run_weapon_popup, image=btn2_image, compound='left', font=btn_font)
btn2.grid(row=2, column=1, padx=20, pady=20)

btn3 = tk.Button(frame1, text='Noise', height=100, width=200, fg='green',
                 command=noise, image=btn3_image, compound='left', font=btn_font)
btn3.grid(row=2, column=2, padx=20, pady=20)

btn4 = tk.Button(frame1, text='Record', height=100, width=200, fg='orange',
                 command=record, image=btn4_image, compound='left', font=btn_font)
btn4.grid(row=3, column=0, padx=20, pady=20)

btn6 = tk.Button(frame1, text='In Out', height=100, width=200, fg='green',
                 command=in_out, image=btn6_image, compound='left', font=btn_font)
btn6.grid(row=3, column=1, padx=20, pady=20)

btn7 = tk.Button(frame1, text="Identify", fg="orange",
                 command=maincall, image=btn7_image, compound='left', height=100, width=200, font=btn_font)
btn7.grid(row=3, column=2, padx=20, pady=20)

btn5 = tk.Button(frame1, height=100, width=200, fg='red',
                 command=window.quit, image=btn5_image, font=btn_font)
btn5.grid(row=4, column=1, padx=20, pady=25)

window.mainloop()