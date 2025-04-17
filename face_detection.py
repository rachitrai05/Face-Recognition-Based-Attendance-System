from flask import Flask, render_template, request, jsonify, send_file
import cv2
import numpy as np
import os
import pickle
import face_recognition
from datetime import datetime
import sqlite3
import base64

app = Flask(__name__)

# # Database setup
# DB_FILE = "database.db"
os.makedirs("static/models", exist_ok=True)

# import sqlit
import sqlite3

DB_FILE = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create the attendance table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# Initialize the database when the app starts
init_db()




# Load or create trained face encodings
ENCODINGS_FILE = "static/models/trained_faces.pkl"
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        known_faces = pickle.load(f)
else:
    known_faces = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    img_data = data.get("image")

    if not name or not img_data:
        return jsonify({"success": False, "message": "Invalid request data"})

    try:
        # Decode the Base64 image
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            print("❌ Image could not be decoded")
            return jsonify({"success": False, "message": "Image decoding failed"})

        # Check if a face is detected
        face_encodings = face_recognition.face_encodings(img)
        # print("Register Name ",name)
        if len(face_encodings) > 0:
            for known_name,known_encoding in known_faces.items():
                # print("Known Names ",known_name)
                match = face_recognition.compare_faces([known_encoding], face_encodings[0])[0]
                if match:
                    return jsonify({"success": False, "message": f"Face is already Exist {known_name}"})
            
            # if face is not matches all the fases in the Pickle then will be register
            known_faces[name] = face_encodings[0]
            with open(ENCODINGS_FILE, "wb") as f:
                pickle.dump(known_faces, f)
            print(f"✅ Face registered for: {name}")
            return jsonify({"success": True, "message": "Face registered!"})

        print("❌ No face detected!")
        return jsonify({"success": False, "message": "No face detected!"})

    except Exception as e:
        print(f"⚠️ Error in register: {str(e)}")
        return jsonify({"success": False, "message": "Internal Server Error"})


@app.route("/recognize", methods=["POST"])
def recognize():
    data = request.json
    img_data = data.get("image")

    if not img_data:
        return jsonify({"success": False, "message": "No image received"})

    # Decode Base64 image
    img_bytes = base64.b64decode(img_data)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"success": False, "message": "Image decoding failed"})

    # Detect faces
    face_encodings = face_recognition.face_encodings(img)
    if len(face_encodings) > 0:
        for name, known_encoding in known_faces.items():
            match = face_recognition.compare_faces([known_encoding], face_encodings[0])[0]
            if match:
                current_date = datetime.now().strftime("%Y-%m-%d")
                current_time = datetime.now().strftime("%H:%M:%S")
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute(f"""INSERT INTO attendance (name, date, time) VALUES ("{name}","{current_date}","{current_time}")""")
                conn.commit()
                conn.close()
                
                print(f"✅ Attendance marked for {name}")  # Debugging

                return jsonify({"success": True, "message": f"Attendance marked for {name} at Time : {current_time}", "name": name})

    return jsonify({"success": False, "message": "Face not recognized!"})

@app.route("/validate",methods =["POST"] )
def validate():
    data = request.json
    img_data = data.get("image")
    
    if not img_data:
        return jsonify({"success": False, "message": "No image received"})
    
      # Decode Base64 image
    img_bytes = base64.b64decode(img_data)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"success": False, "message": "Image decoding failed"})
    
    
    # Detect faces
    face_encodings = face_recognition.face_encodings(img)
    if len(face_encodings) > 0:
        for name, known_encoding in known_faces.items():
            match = face_recognition.compare_faces([known_encoding], face_encodings[0])[0]
            if match:
                if str(name).lower() in  ("anuj gupta", "rachit rai"):
                    
                    print(f"✅ Authenticate User {name}")  # Debugging

                    return jsonify({"success": True, "message": f"Autherized User for Access the Attendance {name}", "name": str(name).lower()})
                else:
                    return jsonify({"success": True, "message": f"UnAuthorized User for Access the Attendance {name}", "name": str(name).lower()})

    return jsonify({"success": False, "message": "Face not recognized!"})
    

@app.route("/export")
def export_attendance():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    data = c.fetchall()
    conn.close()

    filename = "attendance_report.csv"
    with open(filename, "w") as f:
        f.write("ID,     Name,     Date,    Time\n")
        for row in data:
            f.write(f"{row[0]}, {row[1]}, {row[2]},  {row[3]}\n")
    return send_file(filename, as_attachment=True)



@app.route("/attendance/view", methods=["GET"])
def view_attendance():
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Fetch attendance records
    c.execute("SELECT name, date, time FROM attendance ORDER BY date DESC, time DESC")
    records = c.fetchall()
    conn.close()

    # Generate an HTML table
    html = """
    <html>
    <head>
        <title>Attendance Records</title>
        <style>
       body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #ff9a9e, #fad0c4, #fad0c4, #ffdde1);
    text-align: center;
    margin: 0;
    padding: 0;
}

h2 {
    color: #333;
    margin-top: 20px;
}

table {
    width: 80%;
    margin: 20px auto;
    border-collapse: collapse;
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

th {
    background-color: #007bff;
    color: white;
    text-transform: uppercase;
    letter-spacing: 1px;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}

tr:hover {
    background-color: #ddd;
    transition: 0.3s;
}

@media screen and (max-width: 768px) {
    table {
        width: 100%;
    }
    th, td {
        padding: 10px;
    }
}
        </style>
    </head>
    <body>
        <h2>Attendance Records</h2>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Date</th>
                    <th>Time</th>
                </tr>
            </thead>
            <tbody>
    """

    for row in records:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"

    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    return html



if __name__ == "__main__":
    app.run(debug=True)
