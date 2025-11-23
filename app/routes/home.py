from flask import Blueprint, render_template
from app.models import Student

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    all_students = Student.query.all()
    return render_template("home.html", students=all_students)