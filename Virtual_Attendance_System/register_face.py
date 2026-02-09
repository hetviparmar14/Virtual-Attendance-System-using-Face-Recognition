import cv2
import os

name = input("Enter Student Name: ")

path = "dataset/" + name
os.makedirs(path, exist_ok=True)

cam = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        count += 1
        filename = f"{path}/{count}.jpg"
        cv2.imwrite(filename, frame)
        print("Image Saved:", filename)

    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
