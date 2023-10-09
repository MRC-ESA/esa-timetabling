from flask import Flask, render_template

# create a new Flask application instance
app = Flask(__name__)

# define a new Flask route for serving the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# run the application if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)