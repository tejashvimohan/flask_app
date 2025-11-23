from flask import Blueprint, redirect, url_for, flash
from app.models import Student
from app.enroll_face import capture_embedding
from app import db 

face_register_bp = Blueprint('face_register', __name__)

@face_register_bp.route('/register/face/<string:roll_no>', methods =["GET","POST"])
def register_face(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    
    if not student:
        flash("Student Not Found. Please register student detail first.", "danger")
        return redirect(url_for("register.register"))
    
   
    embedding_blob = capture_embedding()
    
    if embedding_blob is None:
        flash("Face capture failed. Try again!", "danger")
        return redirect(url_for("face_register.register_face"))
    
    elif embedding_blob == student.face_embedding:
        flash("Already Registered")
    
    else:
        student.face_embedding = embedding_blob
        db.session.commit()

    flash("Face registered successfully!", "success")
    return redirect(url_for("dashboard.manage_students"))
     
      
    
    
 
        