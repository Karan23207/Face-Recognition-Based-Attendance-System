
from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Directory for storing user data
os.makedirs("UserImages", exist_ok=True)
attendance_file = "attendance.csv"
if not os.path.exists(attendance_file):
    pd.DataFrame(columns=["Name", "Login ID", "Date", "Time"]).to_csv(attendance_file, index=False)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def load_known_faces():
    known_faces = []
    known_ids = []
    for folder in os.listdir("UserImages"):
        folder_path = os.path.join("UserImages", folder)
        if os.path.isdir(folder_path):
            for img_file in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img_file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    known_faces.append(img)
                    known_ids.append(folder)
    return known_faces, known_ids

def match_faces(known_faces, test_face):
    for i, known_face in enumerate(known_faces):
        res = cv2.matchTemplate(test_face, known_face, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > 0.8:
            return i
    return -1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    login_id = request.form['login_id']

    if not name or not login_id:
        return "Please provide both Name and Login ID!"

    user_dir = f"UserImages/{login_id}"
    os.makedirs(user_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < 5:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y + h, x:x + w]
            cv2.imwrite(f"{user_dir}/{count}.jpg", face)

        cv2.imshow("Register User", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return f"User {name} registered successfully!"

@app.route('/mark', methods=['POST'])
def mark_attendance():
    known_faces, known_ids = load_known_faces()
    if not known_faces:
        return "No registered faces found!"

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            test_face = gray[y:y + h, x:x + w]
            match_index = match_faces(known_faces, test_face)

            if match_index != -1:
                login_id = known_ids[match_index]
                # name = login_id.split('_')[0]
                name = login_id 
                time_now = datetime.now()
                date, time = time_now.strftime("%Y-%m-%d"), time_now.strftime("%H:%M:%S")

                df = pd.read_csv(attendance_file)
                if not ((df["Name"] == name) & (df["Date"] == date)).any():
                    df.loc[len(df)] = [login_id,name, date, time]
                    df.to_csv(attendance_file, index=False)
                cap.release()
                cv2.destroyAllWindows()
                return f"Attendance marked for {name}!"


        cv2.imshow("Mark Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "No registered face detected!"

@app.route('/view')
def view_attendance():
    df = pd.read_csv(attendance_file)
    return render_template('view.html', records=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)






