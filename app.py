from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

# Constants
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/teachers'

# Initialize Database with SQLAlchemy
db = SQLAlchemy(app)

# Utility function to check file extension


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Models


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_name = db.Column(db.String(80))
    student_name = db.Column(db.String(80))
    teacher = db.Column(db.String(80))
    date = db.Column(db.String(10))
    time = db.Column(db.String(10))


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    image_filename = db.Column(db.String(120), nullable=True)

# Routes


@app.route("/")
def index():
    """Homepage route."""
    return render_template("index.html")


@app.route('/bookappointment', methods=['GET', 'POST'])
def book_appointment():
    """Route to book an appointment."""
    if request.method == 'POST':
        parent = request.form.get('parent-name')
        student = request.form.get('student-name')
        teacher = request.form.get('teacher')
        date = request.form.get('date')
        time = request.form.get('time')

        new_booking = Booking(
            parent_name=parent,
            student_name=student,
            teacher=teacher,
            date=date,
            time=time
        )
        db.session.add(new_booking)
        db.session.commit()

        booking_data = {
            'id': new_booking.id,
            'parent': new_booking.parent_name,
            'student': new_booking.student_name,
            'teacher': new_booking.teacher,
            'date': new_booking.date,
            'time': new_booking.time
        }
        return jsonify(booking_data)

    return render_template('index.html')


@app.route('/show_appointments/<string:teacher_name>', methods=['GET'])
def show_appointments(teacher_name):
    """Route to show appointments for a specific teacher."""
    appointments = Booking.query.filter_by(teacher=teacher_name).all()
    return render_template('appointments.html', appointments=appointments)


@app.route('/teacher', methods=['GET', 'POST'])
def create_or_edit_teacher():
    """Route to create or edit teacher details."""
    teacher = None
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        department = request.form.get('department')
        image = request.files.get('image')
        filename = None

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        teacher = Teacher(name=name, subject=subject,
                          department=department, image_filename=filename)
        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for('show_teacher', teacher_id=teacher.id))

    return render_template('teacherform.html', teacher=teacher)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Route to serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/teacher/<int:teacher_id>', methods=['GET'])
def show_teacher(teacher_id):
    """Route to show teacher profile."""
    teacher = Teacher.query.get_or_404(teacher_id)
    return render_template('teacherprofile.html', teacher=teacher)


@app.route('/getteachers', methods=['GET'])
def get_teachers():
    """Route to get all teachers."""
    teachers = Teacher.query.all()
    teacher_list = []
    for teacher in teachers:
        teacher_list.append({
            'id': teacher.id,
            'name': teacher.name
        })
    return jsonify(teacher_list)


# Run main application
if __name__ == "__main__":
    app.run(debug=True)
