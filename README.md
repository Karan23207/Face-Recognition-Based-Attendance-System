# Face-Recognition-Based-Attendance-System
This is a Python + Flask-based Face Recognition Attendance System that uses a webcam to register users and mark their attendance by recognizing their faces. 
Attendance records are saved in a CSV file, and users can view all attendance data through a web interface.

 Features :-
1. User Registration via webcam (captures face images)
2. Face Matching using cv2.matchTemplate
3. Live Webcam Feed for face detection
4. Attendance Logging with Date & Time
5. CSV Storage of attendance records
6. Web Interface using HTML + CSS (index and view pages)

 Technologies Used
  * Python 3
  * Flask (for the web server)
  * OpenCV (for face detection and matching)
  * Pandas (for CSV handling)
  * HTML + CSS (for frontend)

Application Workflow
 1. Register User
> Fill in Name and Login ID
>Click Register
>The webcam captures 5 face images and saves them in /UserImages/<login_id>/

 2. Mark Attendance
>Click Start Attendance
>Webcam opens and scans your face
>If a match is found (confidence > 80%), attendance is logged in attendance.csv with:
  * Name
  *Login ID
  *Date
  *Time

 3. View Attendance
>Click View Attendance
>Displays the CSV contents as a table in a separate HTML page.

📁 Project Structure

face-attendance-system/
│
├── UserImages/             # Stores registered face images
├── templates/
│   ├── index.html          # Main UI page
│   └── view.html           # Attendance records page
├── attendance.csv          # Attendance log file
├── app.py                  # Flask backend with OpenCV logic
└── README.md               # This file
Press q to quit the webcam feed while registering or marking attendance.

Minimum 1 registered user is required for face matching to work.

Ensure lighting is proper for better face detection.

⚠️ Limitations
>Uses basic template matching (cv2.matchTemplate) instead of advanced face encodings — performance may vary.
>Not optimized for large-scale or multi-user real-time environments.
>Does not support mobile devices or remote camera feeds.

📢 Future Enhancements
Replace cv2.matchTemplate with FaceNet / Dlib / DeepFace for better accuracy.
>Add admin login and user management
>Store attendance data in SQLite / MySQL
>Add email notifications and analytics dashboards


<img width="1716" height="623" alt="Screenshot 2024-12-13 140946" src="https://github.com/user-attachments/assets/c54c987c-ea00-4a1c-8022-3edb194fcb16" />
<img width="1716" height="623" alt="Screenshot 2024-12-13 140946" src="https://github.com/user-attachments/assets/d93bed9f-5e83-4c2a-aa40-1b8cfab4528d" />






