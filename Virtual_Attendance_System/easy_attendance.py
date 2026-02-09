from deepface import DeepFace
import cv2
import os
import pandas as pd
from datetime import datetime

dataset_path = "dataset"

cap = cv2.VideoCapture(0)

def mark_attendance(name):
    file = "attendance.csv"

    if not os.path.exists(file):
        df = pd.DataFrame(columns=["Name","Time"])
        df.to_csv(file,index=False)

    df = pd.read_csv(file)

    if name not in df["Name"].values:
        time = datetime.now().strftime("%H:%M:%S")
        new_row = {"Name":name,"Time":time}
        df = pd.concat([df,pd.DataFrame([new_row])])
        df.to_csv(file,index=False)

while True:
    ret, frame = cap.read()
    cv2.imshow("Attendance Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):

        cv2.imwrite("temp.jpg", frame)

        result = DeepFace.find(
            img_path="temp.jpg",
            db_path=dataset_path,
            enforce_detection=False
        )

        if len(result[0]) > 0:
            path = result[0]['identity'][0]
            name = path.split("\\")[1]
            print("Detected:", name)
            mark_attendance(name)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
