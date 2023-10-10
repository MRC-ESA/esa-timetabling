from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize a new Flask application
# Flask uses this to determine the root path for the application
# so it can locate related files (templates, static files, etc.)
app = Flask(__name__)

# Configure database details
# SQLALCHEMY_DATABASE_URI is used to set the URI for the database connection
# The string 'sqlite:///bookingsdb.db' indicates using an SQLite database named bookingsdb.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookingsdb.db'

# SQLALCHEMY_TRACK_MODIFICATIONS is set to False to disable Flask-SQLAlchemy's modification tracking
# This is not needed for this application and also saves system resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy ORM instance, passing in the Flask app to bind them
db = SQLAlchemy(app)

# Define models to structure the database using classes
# Each model translates to a table in the database

class Teacher(db.Model):
    # Define columns for the teacher table
    # Each attribute of the class represents a column in the table
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_first_name = db.Column(db.String(50), nullable=False)
    teacher_surname = db.Column(db.String(50), nullable=False)
    teacher_subject = db.Column(db.String(50), nullable=False)
    # Define a relationship to link Teacher and ParentBooking tables on teacher_id
    bookings = db.relationship('ParentBooking', backref='teacher', lazy=True)

class Parent(db.Model):
    # Similar structure to Teacher model, defining columns for the parent table
    parent_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    parent_first_name = db.Column(db.String(50), nullable=False)
    parent_surname = db.Column(db.String(50), nullable=False)
    # Link Parent and ParentBooking tables using parent_id
    bookings = db.relationship('ParentBooking', backref='parent', lazy=True)

class Student(db.Model):
    # Model for students, includes relationships to parents and bookings
    student_id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(50), nullable=False)
    student_surname = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), nullable=False)
    parents = db.relationship('Parent', backref='student', lazy=True)
    bookings = db.relationship('ParentBooking', backref='student', lazy=True)

class Class(db.Model):
    # Model for class details, note the use of class_ as backref since class is a reserved word
    class_id = db.Column(db.Integer, primary_key=True)
    class_number = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    class_floor = db.Column(db.Integer, nullable=False)
    students = db.relationship('Student', backref='class_', lazy=True)

class ParentBooking(db.Model):
    # Model for bookings, linking together teachers, students, and parents
    booking_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.parent_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)

# Define a route decorator to tell Flask which URL should trigger the function below it
# In this case, the root URL ("/") triggers the index() function
@app.route("/")
def index():
    # Use Flask's render_template function to display an HTML file, assumed to be located
    # in a folder named 'templates'
    return render_template("index.html")

# Check if this script is run directly (not imported)
# If true, the Flask application runs with debugging enabled
# Note: In production, debug should be set to False for security reasons
if __name__ == "__main__":
    app.run(debug=True)