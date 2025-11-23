from flask import Blueprint, render_template, Response, current_app, flash, redirect, url_for
import cv2
import numpy as np
from datetime import date, datetime, time
from app import db
from app.models import Attendance, Student, Teacher, Admin  # adapt if names differ
from PIL import Image

attendance_bp = Blueprint('attendance', __name__, template_folder='../templates', url_prefix='/attendance')


def mark_attendance_live():
    print("[INFO] Loading Students from Database...")
    
    # Fetch all students using SQLAlchemy
    all_students = session.query(Student).all()
    
    # Pre-load embeddings into memory to avoid JSON decoding every frame
    known_faces = []
    for student in all_students:
        known_faces.append({
            "id": student.id,
            "name": student.name,
            "embedding": student.get_embedding() # Convert back to list
        })
    
    if not known_faces:
        print("[WARNING] Database is empty. Register students first.")
        return

    cap = cv2.VideoCapture(0)
    recognized_today = {} 
    
    print("[INFO] System Active. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        display_frame = frame.copy()

        try:
            # Detect faces in live frame
            live_faces = DeepFace.represent(
                img_path=frame,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=False
            )
            
            for face_data in live_faces:
                live_embedding = face_data["embedding"]
                
                # Draw logic
                facial_area = face_data.get("facial_area", {})
                x, y, w, h = facial_area.get("x", 0), facial_area.get("y", 0), facial_area.get("w", 0), facial_area.get("h", 0)

                # Compare against DB
                best_match = None
                lowest_distance = 10.0 # Start high

                for student in known_faces:
                    dist = find_cosine_distance(live_embedding, student["embedding"])
                    
                    if dist < lowest_distance:
                        lowest_distance = dist
                        if dist <= THRESHOLD:
                            best_match = student

                if best_match:
                    s_name = best_match["name"]
                    s_id = best_match["id"]
                    color = (0, 255, 0)
                    
                    # Log Attendance via SQLAlchemy
                    if s_id not in recognized_today:
                        new_log = Attendance(student_id=s_id)
                        session.add(new_log)
                        session.commit()
                        
                        recognized_today[s_id] = time.time()
                        print(f"[ACCESS GRANTED] {s_name}")
                    
                    label = f"{s_name} ({round(lowest_distance, 2)})"
                else:
                    color = (0, 0, 255)
                    label = "Unknown"

                cv2.rectangle(display_frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(display_frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        except ValueError:
            pass # No face found
        except Exception:
            pass

        cv2.imshow("Attendance (SQLAlchemy)", display_frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- MAIN ---
if __name__ == "__main__":
    mode = input("Enter '1' to Register, '2' to Mark Attendance: ")
    
    if mode == '1':
        uid = input("Enter User ID: ")
        uname = input("Enter User Name: ")
        register_student_ui(uid, uname)
    elif mode == '2':
        mark_attendance_live()








   



