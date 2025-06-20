import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk  # For adding logo

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass123",
    database="cctv_db"
)
cursor = conn.cursor()

# Function to sign up a user
def signup_user():
    username = signup_username.get()
    password = signup_password.get()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "User already exists! Please try logging in.")
        return

    # Insert new user into the database
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    messagebox.showinfo("Success", "Signup successful! Please log in.")
    signup_window.destroy()

# Function to log in a user
def login_user():
    username = login_username.get()
    password = login_password.get()

    # Check if the user exists and the password matches
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login", "Login successful!")
        main_window.destroy()
        execute_main_gui()
    else:
        messagebox.showerror("Login", "Invalid username or password!")

# Function to show the signup window
def show_signup():
    global signup_window, signup_username, signup_password
    signup_window = tk.Toplevel(main_window)
    signup_window.title("Signup")
    signup_window.geometry("500x600")  # Increased window size for better layout
    signup_window.configure(bg='#e3f2fd')  # Light blue background for a clean look

    # Adding the logo to the signup window
    logo_image = Image.open("icons/spy.png")
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(signup_window, image=logo_photo, bg='#e3f2fd')
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=20)

    # Title for signup form
    tk.Label(signup_window, text="Create an Account", font=("Helvetica", 24, 'bold'), fg="#34495e", bg='#e3f2fd').pack(pady=10)

    # Create a frame for the form
    signup_frame = tk.Frame(signup_window, bg='#e3f2fd')
    signup_frame.pack(pady=10)

    # Username field
    tk.Label(signup_frame, text="Username", font=("Helvetica", 14), fg="#34495e", bg='#e3f2fd').grid(row=0, column=0, padx=10, pady=10)
    signup_username = ttk.Entry(signup_frame, style="TEntry")
    signup_username.grid(row=0, column=1, padx=10, pady=10)

    # Password field
    tk.Label(signup_frame, text="Password", font=("Helvetica", 14), fg="#34495e", bg='#e3f2fd').grid(row=1, column=0, padx=10, pady=10)
    signup_password = ttk.Entry(signup_frame, style="TEntry", show="*")
    signup_password.grid(row=1, column=1, padx=10, pady=10)

    # Signup Button
    signup_button = ttk.Button(signup_window, text="Signup", style="TButton", command=signup_user)
    signup_button.pack(pady=20)

# Function to execute the Smart CCTV Tkinter GUI
def execute_main_gui():
    print("Launching Smart CCTV Application...")
    import main  # Assuming your Tkinter code for CCTV is saved in 'smart_cctv.py'

# Main Window (Login Page)
main_window = tk.Tk()
main_window.title("Smart CCTV - Login")
main_window.geometry("600x700")  # Increased window size for login
main_window.configure(bg='#f5f5f5')

# Load and place the CCTV logo
logo_image = Image.open("icons/spy.png")
logo_image = logo_image.resize((120, 120), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(main_window, image=logo_photo, bg='#f5f5f5')
logo_label.pack(pady=20)

# Title Label
main_title = tk.Label(main_window, text="Smart CCTV", font=("Helvetica", 30, 'bold'), fg="#34495e", bg='#f5f5f5')
main_title.pack(pady=10)

# Create a frame for the login form
login_frame = tk.Frame(main_window, bg='#ffffff', bd=10, relief="groove")
login_frame.pack(pady=20)

# Title Label for the login section
login_title = tk.Label(login_frame, text="Login", font=("Helvetica", 24, 'bold'), fg="#34495e", bg='#ffffff')
login_title.grid(row=0, column=0, columnspan=2, pady=20)

# Username Entry
tk.Label(login_frame, text="Username", font=("Helvetica", 14), fg="#34495e", bg='#ffffff').grid(row=1, column=0, pady=10, padx=10)
login_username = ttk.Entry(login_frame, style="TEntry")
login_username.grid(row=1, column=1, pady=10, padx=10)

# Password Entry
tk.Label(login_frame, text="Password", font=("Helvetica", 14), fg="#34495e", bg='#ffffff').grid(row=2, column=0, pady=10, padx=10)
login_password = ttk.Entry(login_frame, style="TEntry", show="*")
login_password.grid(row=2, column=1, pady=10, padx=10)

# Login Button
login_button = ttk.Button(login_frame, text="Login", style="TButton", command=login_user)
login_button.grid(row=3, column=0, columnspan=2, pady=20)

# Signup Button
signup_button = ttk.Button(main_window, text="Signup", style="TButton", command=show_signup)
signup_button.pack(pady=10)

# Adding styles for modern look
style = ttk.Style()
style.configure("TEntry", padding=10, relief="flat", borderwidth=0, background="#ecf0f1")
style.configure("TButton", padding=10, relief="flat", background="#2980b9", foreground="white", font=("Helvetica", 12, "bold"), borderwidth=0)
style.map("TButton", background=[('active', '#3498db')])

main_window.mainloop()

# Close the database connection
conn.close()
