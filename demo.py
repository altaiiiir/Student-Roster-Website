import psycopg2
from flask import Flask, redirect, url_for, render_template, request, session, flash
import func
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


#execute courses query
cur.execute('Select * from Course_Catalog')
courseRows = cur.fetchall()

#execute transcripts query
cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_Catalog.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
FROM Transcript
	JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
	JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)
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
        session.permanant = True
        user = request.form["nm"]
        # if user==''
        session["user"] = user
        return render_template("studentPage.html", things=rows)
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



@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("studentPage"))

@app.route("/Transcript", methods=["POST", "GET"])
def Transcript():
    if request.method == "POST":
        if 'delete' in request.form:
            studentID = int(request.form["studentID"])
            SLN = request.form["SLN"]
            section = request.form["section"]
            cur.execute('SELECT ID FROM Course_Info WHERE SLN = %s AND Section = %s', (SLN, section))
            classIDs = cur.fetchall()
            classID = classIDs[0][0]
            cur.execute('''DELETE FROM Transcript WHERE classID = %s AND studentID = %s''', (int(classID), studentID))
            cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_Catalog.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                            FROM Transcript
                                JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                                JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)
                                JOIN Student ON (Transcript.StudentID = Student.ID)""")
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
            cur.execute('''INSERT INTO Transcript (StudentID, ClassID, FinalGrade)
                                Values(%s, %s, %s)''', (studentID, int(classID), grade))
            cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_Catalog.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                            FROM Transcript
                                JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                                JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)
                                JOIN Student ON (Transcript.StudentID = Student.ID)""")
            updatedTranscriptRows = cur.fetchall()
            return render_template("Transcripts.html", things=updatedTranscriptRows)
    else:        
        return render_template("Transcripts.html", things=transcriptRows) 

@app.route("/BehaviorNotes", methods=["POST", "GET"])
def studentNotes():
    if request.method == "POST":
        if 'viewNotes' in request.form:
            render_template("BehaviorNotes.html")
        else:
            print ("hi")
    else:
        studentNotes = func.viewStudentNotes()
        return render_template("BehaviorNotes.html", things=studentNotes)
    return render_template("BehaviorNotes.html")



if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()