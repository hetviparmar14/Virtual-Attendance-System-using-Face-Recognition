import tkinter as tk
from tkinter import messagebox
from deepface import DeepFace
import cv2
import os
import sqlite3
from datetime import datetime

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    name TEXT,
    date TEXT,
    time TEXT,
    lecture TEXT
)
""")
conn.commit()

# ---------- CAMERA ----------
cap = None

dataset_path = "dataset"

# ---------- FUNCTIONS ----------

def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    show_frame()

def show_frame():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera", frame)
        root.after(10, show_frame)

def scan_face():
    global cap
    if cap is None:
        messagebox.showerror("Error","Start camera first")
        return

    ret, frame = cap.read()
    cv2.imwrite("temp.jpg", frame)

    try:
        result = DeepFace.find(
            img_path="temp.jpg",
            db_path=dataset_path,
            enforce_detection=False
        )

        if len(result[0]) > 0:
            path = result[0]['identity'][0]
            name = path.split("\\")[1]

            date = datetime.now().strftime("%d-%m-%Y")
            time = datetime.now().strftime("%H:%M:%S")
            lecture = lecture_entry.get()

            cursor.execute(
                "INSERT INTO attendance VALUES (?,?,?,?)",
                (name, date, time, lecture)
            )
            conn.commit()

            messagebox.showinfo("Success", f"Attendance Marked for {name}")

        else:
            messagebox.showwarning("No Match","Face not found")

    except:
        messagebox.showerror("Error","Face scan failed")

def stop_camera():
    global cap
    if cap:
        cap.release()
        cv2.destroyAllWindows()

# ---------- GUI ----------
root = tk.Tk()
root.title("Virtual Attendance System")
root.geometry("350x250")

tk.Label(root,text="Lecture Name",font=("Arial",12)).pack(pady=10)

lecture_entry = tk.Entry(root,font=("Arial",12))
lecture_entry.pack()

tk.Button(root,text="Start Camera",command=start_camera,width=20).pack(pady=10)
tk.Button(root,text="Scan Face",command=scan_face,width=20).pack(pady=5)
tk.Button(root,text="Stop Camera",command=stop_camera,width=20).pack(pady=5)

root.mainloop()
