from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

# create a new Flask application instance
app = Flask(__name__)

# configure the application to use a SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///timetabling.db"

# create a new SQLAlchemy database instance
db = SQLAlchemy(app)

# define a new database model for bookings
class Bookings(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    parent_name = db.Column(db.String(80), nullable=False)
    student_name = db.Column(db.String(80), nullable=False)
    teacher = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time = db.Column(db.Time, nullable=False, default=time.min)
    def __repr__(self):
        return f"<Booking {self.id}>"

# define a new Flask route for serving the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# run the application if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)