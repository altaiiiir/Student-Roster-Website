from flask import Flask, render_template, redirect, url_for, request
import psycopg2
import func
app = Flask(__name__)

con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/home") 
def home():
    return render_template("home.html")

@app.route("/courseCatalog", methods = ["POST", "GET"])
def courseCatalog():
    if request.method == "POST":
        user = request.form["nm"]
    else:
        courseCatalog = func.viewCourseCatalog()
        return render_template("courseCatalog.html", things=courseCatalog)

@app.route("/studentPage", methods =['GET', 'POST'])
def students():
    if request.method == "POST":
        user = request.form["nm"]
    else:
        rows = func.viewAllStudents()
        return render_template("studentPage.html", things = rows)

if __name__ == "__main__":
     app.run(debug =True)