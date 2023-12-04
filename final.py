
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import joblib
from subprocess import call
import webbrowser  # Import the webbrowser module

import mediapipe as mp
import pyautogui
import os
import datetime

# Load the pre-trained SVM model and LabelEncoder
svm_model = SVC(kernel='linear')
svm_model = joblib.load('svm_model.pkl')

encoder = LabelEncoder()
encoder.classes_ = np.load('encoder_classes.npy')

# Initialize camera
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    # ... (your existing code)

    for (x, y, w, h) in faces:
        face_roi = gray_frame[y:y+h, x:x+w]

        resized_face_roi = cv2.resize(face_roi, (64, 64))
        flattened_face_roi = resized_face_roi.flatten()

        # Reshape the flattened face ROI to a 2D array
        flattened_face_roi_2d = flattened_face_roi.reshape(1, -1)

        predicted_label = svm_model.predict(flattened_face_roi_2d)
        predicted_person = encoder.inverse_transform([predicted_label])[0]

    # ... (rest of your code)

        # Display the identified person's name
        cv2.putText(frame, f"Identified: {predicted_person}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Perform further processes based on the identified person
        if predicted_person == "alpha":
            cv2.putText(frame, "Welcome, alpha!", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Face Authentication", frame)
            cv2.waitKey(2000)  # Show the "Welcome" message for 2 seconds
            cap.release()  # Release the camera resources
            cv2.destroyAllWindows()


            # Run another Python script
            def open_py_file():
                call(["python","combine_PHOTO_&_DROWING.py"])

            open_py_file()
            # os.system('python "combine_PHOTO_&_DROWING.py"')

            exit()
        # if predicted_person == "alpha":
        #     cv2.putText(frame, "Welcome, alpha!", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        #     webbrowser.open("combine_PHOTO_&_DROWING_.PY")  # Open a link for alpha
        #     break
        #     # Perform actions for John
        # elif predicted_person == "pk":
        #     cv2.putText(frame, "Hello, pk!", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        #     # Perform actions for Jane
        #     break
        else:
            cv2.putText(frame, "Unknown Person", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Handle unknown person

    cv2.imshow("Face Authentication", frame)

    # Exit real-time authentication when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
