from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookingsdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_first_name = db.Column(db.String(50), nullable=False)
    teacher_surname = db.Column(db.String(50), nullable=False)
    teacher_subject = db.Column(db.String(50), nullable=False)
    bookings = db.relationship('ParentBooking', backref='teacher', lazy=True)

class Parent(db.Model):
    parent_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    parent_first_name = db.Column(db.String(50), nullable=False)
    parent_surname = db.Column(db.String(50), nullable=False)
    bookings = db.relationship('ParentBooking', backref='parent', lazy=True)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(50), nullable=False)
    student_surname = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), nullable=False)
    parents = db.relationship('Parent', backref='student', lazy=True)
    bookings = db.relationship('ParentBooking', backref='student', lazy=True)

class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    class_number = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    class_floor = db.Column(db.Integer, nullable=False)
    students = db.relationship('Student', backref='class_', lazy=True)

class ParentBooking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.parent_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/bookappointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        booking = request.get_json()
        # Do something with booking (e.g., save to database)
        print(booking)
        return render_template('bookingform.html', booking=booking)

if __name__ == "__main__":
    app.run(debug=True)