import face_recognition
import cv2
import os
import numpy as np

# =========================
# LOAD DATASET
# =========================

dataset_path = "dataset"

known_encodings = []
known_names = []

if not os.path.exists(dataset_path):
    print("Dataset folder not found!")
    exit()

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_folder):
        continue

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(person_name)

print("✅ Dataset Loaded Successfully")

# =========================
# START CAMERA
# =========================

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        name = "Unknown"
        color = (0, 0, 255)  # Red for unknown

        if len(known_encodings) > 0:

            # Compare faces
            matches = face_recognition.compare_faces(
                known_encodings,
                face_encoding,
                tolerance=0.5   # Adjust if needed
            )

            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_names[best_match_index]
                color = (0, 255, 0)  # Green for recognized

        # Draw rectangle
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Show name
        cv2.putText(frame, name,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2)

    cv2.imshow("Face Scanner", frame)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

video.release()
cv2.destroyAllWindows()
