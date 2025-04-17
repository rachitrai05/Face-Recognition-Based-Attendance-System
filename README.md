# Face-Recognition-Based-Attendance-System
📌 Project Description

This project is a **Face Recognition-Based Attendance System** that automates attendance marking using facial recognition technology. Built with Python, OpenCV, and the `face_recognition` library, the system captures a user's face through the webcam, matches it with the registered dataset, and logs attendance in real-time.The Face Recognition-Based Attendance System is a contactless and intelligent solution for managing attendance using facial recognition technology. It eliminates the need for traditional roll calls or manual entries by automating the process through real-time face detection and verification.Designed especially for classrooms, training programs, and office environments, this system streamlines attendance logging while ensuring accuracy and security.
## 

It eliminates manual attendance processes and provides a **contactless**, **secure**, and **efficient** way to track presence, making it ideal for use in classrooms, offices, and training programs.

---

## 🎯 Features

- 👤 **User Registration**  
  Capture and store face images with user-provided names for future recognition.

- 🎥 **Live Face Detection**  
  Detects faces in real-time using a webcam.

- 🧠 **Face Recognition**  
  Compares live face encodings with stored data for 1:1 matching.

- 📝 **Attendance Logging**  
  Automatically marks the date and time of attendance when a face is recognized.

- 💾 **CSV Export**  
  Exports attendance data into a `.csv` file for easy tracking and reporting.

- 🌐 **Web-Based Interface**  
  Built using Flask, with live video streaming, face registration, and attendance management through a simple UI.

---

## 🛠️ Technologies Used

- Python  
- OpenCV  
- face_recognition  
- Flask  
- face-api.js  
- HTML, CSS (Tailwind CSS)  
- JavaScript  

## 📷 How It Works

1. User starts the recognition system through the web interface.
2. The webcam captures live video feed.
3. The system detects faces in real-time.
4. If a detected face matches an existing face in the system’s database, attendance is marked in a CSV file.
5. Attendance can be viewed/exported by the admin.

---

## 📁 Project Structure
Face-Recognition-Attendance-System/
│
├── 📂 static/                       # Static files (CSS, JavaScript, images)
│   ├── 📂 css/
│   │   └── style.css               # Custom styling for the web interface
│   ├── 📂 js/
│   │   └── face_detection.js       # JavaScript for face-api.js integration
│   └── 📂 attendance_bg.jpg        # Background image for the UI
│
├── 📂 templates/
│   └── index.html                  # Web interface for face registration and attendance
│
├── 📂 Faces/                       # Folder to store registered user images
│
├── 📂 Attendance/                  # Logs attendance CSV and export files
│   └── attendance.csv             # Generated file with attendance data
│
├── Face_detection.py              # Flask backend to manage routes and logic
├── encode_faces.py                # Script to encode and store face encodings
├── README.md                      # Project documentation
├── requirements.txt               # List of dependencies
└── log.txt                        # Optional: Plain text log of attendance (for backup/debugging)

🖥️Installation

# Clone the repository:
git clone https://github.com/yourusername/Face-Recognition-Attendance-System.git
cd Face-Recognition-Attendance-System

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python Face_detection.py

Access the web interface:
Open in Browser
Navigate to: http://127.0.0.1:5000

✅ Result
The Face Recognition-Based Attendance System successfully achieved its objective of automating attendance marking using facial recognition technology. The system demonstrated high accuracy and reliability during testing, providing a seamless and secure experience for both users and administrators.

🤝Contributing
Contributions are welcome! If you have any ideas or improvements, feel free to create an issue or submit a pull request.
