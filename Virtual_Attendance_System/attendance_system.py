import face_recognition
import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime

path = "dataset"
images = []
classNames = []

myList = os.listdir(path)

for person in myList:
    person_folder = os.path.join(path, person)
    for img_name in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_name)
        img = cv2.imread(img_path)
        images.append(img)
        classNames.append(person)

print("Students Loaded:", set(classNames))


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    file = "attendance/attendance.csv"

    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("Name,Time\n")

    df = pd.read_csv(file)

    if name not in df['Name'].values:
        now = datetime.now()
        timeString = now.strftime('%H:%M:%S')
        with open(file, "a") as f:
            f.write(f"{name},{timeString}\n")


print("Encoding Faces...")
encodeListKnown = findEncodings(images)
print("Encoding Complete")

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(img, name, (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            markAttendance(name)

    cv2.imshow("Virtual Attendance System", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
