from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.models import Student, Teacher, Admin

#blueprint object
auth_bp = Blueprint('auth', __name__)

#route for login"
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
         
        user = None
         
        if user_type == 'admin':
            user = Admin.query.filter_by(email=email, password=password).first()
            if user:
                session['user_id'] = user.id
                session['user_type'] = 'admin'
                session['user_name'] = user.username
                flash("Login successful!", "success")
                return redirect(url_for('dashboard.admin_dashboard'))
            else:
                flash("Invalid credentials", "danger")
                
        elif user_type == 'teacher':
            user = Teacher.query.filter_by(email=email, password=password).first()   
            if user:
                session['user_id'] = user.id
                session['user_type'] = 'teacher'
                session['user_name'] = user.name
                flash("Login successful!", "success")
                return redirect(url_for('dashboard.teacher_dashboard'))
            else:
                flash("Invalid credentials", "danger")
             
        elif user_type== 'student':
            user = Student.query.filter_by(email=email, password=password).first()  
            if user:
                session['user_id'] = user.id
                session['user_type'] = 'student'
                session['user_name'] = user.name
                flash("Login successful!", "success")
                return redirect(url_for('dashboard.student_dashboard'))
            else:
                flash("Invalid credentials", "danger")
             
        else:
            flash('Please select a valid user type.','info')
            
    return render_template('newlog.html')

#route for logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged Out')
    return redirect(url_for('auth.login'))
