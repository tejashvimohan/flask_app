from flask import  Blueprint, request, render_template, flash, redirect, url_for
from app import db
from app.models import Admin, Teacher, Student


# creating blueprint 
register_bp = Blueprint('register', __name__)

#route for registering user
@register_bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        user_type = request.form.get('user_type')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        roll_no = request.form.get('roll_no')
        
        
        #For registering admin
        if user_type == "admin":
             
            if  Admin.query.filter_by(email=email).first():
                flash('Email already registerd. Please try with different email.', 'error')
                return redirect(url_for('register.register'))
        
            new_user = Admin(username=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Admin Registered Successfully.', 'success')
        
        #for registering teacher   
        elif user_type == "teacher":
            
            if Teacher.query.filter_by(email=email).first():
                flash('Email already registerd. Please try with different email.', 'error')
                return redirect(url_for('register.register'))
                
            new_user = Teacher(name=name, email=email,  password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Teacher Registered Successfully.', 'success')
        
        #for registering student    
        elif user_type == "student":
            
            if Student.query.filter_by(email=email).first():
                flash('Email already registerd. Please try with different email.', 'error')
                return redirect(url_for('register.register'))
            
            new_user = Student(name=name, email=email, password=password, roll_no=roll_no)
            
            db.session.add(new_user)
            db.session.commit()
            flash('Student Registered Successfully.', 'success')
            
        else:
            flash('Invalid User Type. Please enter valid type.', 'error')

        return redirect(url_for("auth.login"))
        
    return render_template("registration.html")
            
        