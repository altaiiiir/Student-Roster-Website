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