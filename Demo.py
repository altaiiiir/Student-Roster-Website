import psycopg2
from flask import Flask, redirect, url_for, render_template, request

# connect to the local host db
con = psycopg2.connect(
    host="database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
    database="webdb",
    user="postgres",
    password="2fD9vPoMU6HAfMM"
)

# cursor
cur = con.cursor()

# execute query
cur.execute('Select * from Student')
rows = cur.fetchall()

for r in rows:
    print(f"ID {r[0]} name {r[1]}")

# execute query
cur.execute('Select * from Course_Catalog')
courseRows = cur.fetchall()

for r in courseRows:
    print(f"SLN {r[0]} Name {r[1]} CourseCredits {r[2]} Type {r[3]}")

# execute query
cur.execute(
    'Select * from Course_Info '
    '   JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)')
courseInfoRows = cur.fetchall()

# execute query
cur.execute(
    'SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)'
    '   JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) '
    '   JOIN Student ON (Student.ID = Transcript.StudentID) '
    'WHERE Course_Info.SLN = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

#execute query
cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)')
courseInfoRows = cur.fetchall()

#execute query
cur.execute('SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN) JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) JOIN Student ON (Student.ID = Transcript.StudentID) WHERE Course_Info.SLN = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

# close cursor
cur.close()

# close the connection
con.close()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("Home.html", things=rows)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("Login.html")


@app.route("/course-catalog", methods=["POST", "GET"])
def courses_catalog():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("CourseCatalog.html", things=courseRows)

@app.route("/course-info")
def courseInfo():
    return render_template("courseInfo.html", things = courseInfoRows)

@app.route("/student-page", methods=["POST", "GET"])
def student_page():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("StudentPage.html", things=rows)


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr} </h1>"


if __name__ == "__main__":
    app.run(debug=True)
