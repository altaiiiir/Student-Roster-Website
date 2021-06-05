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


def showCourseInfoRows():
    cur.execute(
        'Select * from Course_Info '
        '   JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)'
        'ORDER BY Course_Catalog.Name')
    courseInfoRows = cur.fetchall()
    return courseInfoRows

# execute query
cur.execute(
    'SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)'
    '   JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) '
    '   JOIN Student ON (Student.ID = Transcript.StudentID) '
    'WHERE Course_Info.CourseID = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

#execute query
cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)')
courseInfoRows = cur.fetchall()

#execute query
cur.execute('SELECT * FROM Course_Info'
            '   JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID) '
            '   JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) '
            '   JOIN Student ON (Student.ID = Transcript.StudentID) '
            'WHERE Course_Info.CourseID = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

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
def course_info():
    return render_template("CourseInfo.html", things=showCourseInfoRows())
    

@app.route("/student-page", methods=["POST", "GET"])
def student_page():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("StudentPage.html", things=rows)


@app.route("/update-class", methods=["POST", "GET"])
def update_course():
    if request.method == "POST":
        if 'add' in request.form:
            #TODO double check data, protect against sql injections
            #TODO double check if values are legit
            StuID = request.form["studentID"]
            Fname = request.form["first"]
            Lname = request.form["last"]
            gender = request.form["gender"]
            super = request.form["super"]
            alias = request.form["alias"]
            dob = request.form["dob"]

            cur.execute('INSERT INTO Student (StudentID, FirstName, LastName, Alias, \
                Gender, SuperPower, DOB, IsCurrentlyEnrolled,adminID) \
                Values(%s,%s,%s,%s,%s,%s,%s,TRUE,1)',(int(StuID),Fname,Lname,alias,gender,super,dob))
            con.commit()
            return redirect(url_for("viewStudent"))
        else:
            #TODO to double check data, protect against sql injections
            #TODO double check if value is legit
            studID = int(request.form["studID"])
            cur.execute('DELETE FROM Transcript WHERE Transcript.StudentID = %s',[studID])
            # Find the noteID based on studentID, use that to delete notes
            # cur.execute('DELETE FROM Notes WHERE Student_Notes.StudentID = %s',[studID])
            cur.execute('DELETE FROM Student_Notes WHERE Student_Notes.StudentID = %s',[studID])
            cur.execute('DELETE FROM STUDENT WHERE ID = %s',[studID])
            con.commit()
            return redirect(url_for("viewStudent"))
            # currSln = request.form["sln"]
            # newCourseName = request.form["CourseName"]
            # newSection = request.form["Section"]
            # newRoomID = request.form["RoomID"]
            # newInstructorName = request.form["InstructorName"]
            # newTime = request.form["Time"]
            # newQuarter = request.form["Quarter"]
            # newYear = request.form["Year"]

            # if newCourseName is not "":
            #     cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [newCourseName])
            #     tempCourseID = cur.fetchall()
            #     newCourseID = tempCourseID[0][0]
            #     cur.execute('UPDATE Course_Info SET CourseID = %s WHERE sln = %s', (newCourseID, currSln))

            # if newSection is not "":
            #     cur.execute('UPDATE Course_Info SET Section = %s WHERE sln = %s', (newSection, currSln))

            # if newRoomID is not "":
            #     cur.execute('UPDATE Course_Info SET RoomID = %s WHERE sln = %s', (newRoomID, currSln))

            # if newInstructorName is not "":
            #     cur.execute('UPDATE Course_Info SET InstructorName = %s WHERE sln = %s', (newInstructorName, currSln))

            # if newTime is not "":
            #     cur.execute('UPDATE Course_Info SET Time = %s WHERE sln = %s', (newTime, currSln))

            # if newQuarter is not "":
            #     cur.execute('UPDATE Course_Info SET Quarter = %s WHERE sln = %s', (newQuarter, currSln))

            # if newYear is not "":
            #     cur.execute('UPDATE Course_Info SET Year = %s WHERE sln = %s', (newYear, currSln))

            # con.commit()
            # return render_template("CourseInfo.html", things=showCourseInfoRows())
    else:
        return render_template("UpdateClass.html")


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr} </h1>"


if __name__ == "__main__":
    app.run(debug=True)

# close cursor
cur.close()

# close the connection
con.close()
