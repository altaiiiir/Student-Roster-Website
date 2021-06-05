import psycopg2
from flask import Flask, redirect, url_for, render_template, request, session, flash

from datetime import timedelta

from datetime import date

today = date.today()
print("Today's date:", today)

#connect to the local host db
con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

#cursor
cur = con.cursor()

#execute query
cur.execute('Select * from Student')
rows = cur.fetchall()

for r in rows:
   print(f"ID {r[0]} name {r[1]}")

#execute courses query
cur.execute('Select * from Course_Catalog')
courseRows = cur.fetchall()

#execute transcripts query
cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
FROM Transcript
	JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
	JOIN Course_Catalog ON (Course_Info.courseID = Course_Catalog.ID)
	JOIN Student ON (Transcript.StudentID = Student.ID)""")
transcriptRows = cur.fetchall()


app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/") 
def home():
    return render_template("index.html", things=rows)

@app.route("/studentPage", methods=["POST", "GET"]) 
def studentPage():
    if request.method == "POST":
        if 'add' in request.form:
            studentID = request.form['id']
            firstname = request.form['firstnm']
            lastname = request.form['lastnm']
            alias = request.form['alias']
            gender = request.form['gender']
            superpower = request.form['superpower']
            dob = request.form['dob']
            enrolled = request.form['enrolled']
            print(studentID + " " + firstname + " " + lastname + " " + alias + " " + gender + " " + superpower + " " + dob + " " + enrolled)
            cur.execute("""INSERT INTO Student (studentID, firstName, lastName, alias, gender, superpower, dob, iscurrentlyenrolled, adminID)
                        Values (%s, %s, %s, %s, %s, %s, %s, %s, 1)""", (studentID, firstname, lastname, alias, gender, superpower, dob, enrolled))
            cur.execute('Select * from Student')
            updatedStudentrows = cur.fetchall()
            return render_template("studentPage.html", things=rows)
        else:
            studentID = request.form['id']
            firstname = request.form['firstnm']
            lastname = request.form['lastnm']
            alias = request.form['alias']
            gender = request.form['gender']
            superpower = request.form['superpower']
            dob = request.form['dob']
            enrolled = request.form['enrolled']
            cur.execute('''DELETE FROM Student WHERE studentID = %s''', [studentID])
            cur.execute('Select * from Student')
            updatedStudentrows = cur.fetchall()
            return render_template("studentPage.html", things=updatedStudentrows)
    else:
        return render_template("studentPage.html", things=rows)
    
# @app.route("/test")
# def test():
#     return render_template("new.html")

@app.route("/courseCatalog", methods=["POST", "GET"])
def courseCatalog():
    if request.method == "POST":
        creditType = request.form["courseType"]
        SLN = request.form["SLN"]
        cur.execute('Select * from Course_Catalog WHERE Type = %s AND SLN = %d', (creditType, SLN))
        creditRows = cur.fetchall()
        for r in creditRows:
            print(f"ID {r[0]} name {r[1]}")
        return render_template("courseCatalog.html", things=creditRows)
    else:
        return render_template("courseCatalog.html", things=courseRows) 

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user} </h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("studentPage"))

@app.route("/TranscriptAddRemove", methods=["POST", "GET"])
def TranscriptAddRemove():
    if request.method == "POST":
        if 'delete' in request.form:
            studentID = request.form["studentID"]
            SLN = request.form["SLN"]
            section = request.form["section"]
            cur.execute('SELECT ID FROM Course_Info WHERE SLN = %s AND Section = %s', (SLN, section))
            classIDs = cur.fetchall()
            classID = classIDs[0][0]
            cur.execute('''DELETE FROM Transcript WHERE classID = %s AND studentID = %s''', (int(classID), studentID))
        elif 'filterAll' in request.form:
            studentID = int(request.form["studentID"])
            cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                            FROM Transcript
                                JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                                JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                                JOIN Student ON (Transcript.StudentID = Student.ID)
                            WHERE student.id = %s""", [studentID])
            updatedTranscriptRows = cur.fetchall()
            return render_template("Transcripts.html", things=updatedTranscriptRows)
        elif 'filterCur' in request.form:
            studentID = int(request.form["studentID"])
            cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                            FROM Transcript
                                JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                                JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                                JOIN Student ON (Transcript.StudentID = Student.ID)
                            WHERE student.id = %s AND transcript.finalGrade IS NULL""", [studentID])
            updatedTranscriptRows = cur.fetchall()
            return render_template("Transcripts.html", things=updatedTranscriptRows)
        elif 'filterCor' in request.form:
            SLN = int(request.form["SLN"])
            cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                            FROM Transcript
                                JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                                JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                                JOIN Student ON (Transcript.StudentID = Student.ID)
                            WHERE course_info.SLN = %s""", [SLN])
            updatedTranscriptRows = cur.fetchall()
            return render_template("Transcripts.html", things=updatedTranscriptRows)
        else:
            studentID = int(request.form["studentID"])
            SLN = request.form["SLN"]
            section = request.form["section"]
            grade = request.form["grade"]
            cur.execute('SELECT ID FROM Course_Info WHERE SLN = %s AND Section = %s', (SLN, section))
            classIDs = cur.fetchall()
            classID = classIDs[0][0]
            #adds either a grade with null or with a final grade
            if grade == '':
                cur.execute('''INSERT INTO Transcript (StudentID, ClassID)
                    Values(%s, %s)''', (studentID, int(classID)))
            else:
                cur.execute('''INSERT INTO Transcript (StudentID, ClassID, FinalGrade)
                                Values(%s, %s, %s)''', (studentID, int(classID), grade))
        
        redirect(url_for("Transcript"))
    else:        
        return render_template("Transcriptaddremove.html") 

@app.route("/Transcript", methods=["POST", "GET"])
def Transcript():
    cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                    FROM Transcript
                        JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                        JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                        JOIN Student ON (Transcript.StudentID = Student.ID)""")
    updatedTranscriptRows = cur.fetchall()
    return render_template("Transcripts.html", things=updatedTranscriptRows)

if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()