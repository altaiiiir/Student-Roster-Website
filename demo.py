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


gettingIDQuery= "Select ID, firstname, lastname, alias from Student where firstname = %s"
allStudentsQuery = "Select * from Student"
#execute query
cur.execute(allStudentsQuery)
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

findMaxNoteID = """Select MAX(NoteID) from Student_Notes"""
cur.execute(findMaxNoteID)
maxNotInForm = cur.fetchall()
max = maxNotInForm[0][0] #get max note because idk how we are keeping track of noteID
print(max)

func.viewAdmin()

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
        theStudentID = request.form["theirID"]
        note = request.form["notes"]
        noteType = request.form["noteType"]
        session["user"] = user
        if 'viewNotes' in request.form:
            studentNotes = func.viewStudentNotes() #this calls method in func which just returns all student notes

            return render_template("studentNotes.html", things=studentNotes) #renders studentNotes page
        elif 'viewStudentName' in request.form:
            specificStudent = "Select * from Student where Student.FirstName = %s AND Student.StudentID = %s" 
            cur.execute(specificStudent, (user,theStudentID)) # view the student based on their firstName and id
            studentNotes = cur.fetchall()
            
            return render_template("studentPage.html", things=studentNotes) #returns query of that user and studentID to studentPage
        #I need to add a studentNoteInput.html page that asks user for the Note, and the type 
        elif 'add' in request.form:
            findMaxNoteID = """Select MAX(NoteID) from Note""" #find max note from Note  
            cur.execute(findMaxNoteID)
            maxNotInForm = cur.fetchall()
            max = maxNotInForm[0][0] #get max note because idk how we are keeping track of noteID
            max = max + 1
            adminID = 1
            currentDate = date.today()
            studentInsert = """INSERT INTO Note (NoteID, Note, Date, Type, AdminID)
                                Values(%s, %s, %s, %s, %s)""" #OKAY so apparently I need to insert into Note first and then connect that to Student Notes
                                                  #by creating the note and then saying "insert into student_Notes where the Student_Notes.NoteID == Note.ID (the note that I just created in the Note table"  
            
            cur.execute(studentInsert, (max, note, currentDate, noteType, adminID )) #here trying to insert the studentID and notID into the student_notes table 
            con.commit()
            allStudents = func.viewAllStudents()
            return render_template("studentPage.html", things=allStudents)
        return render_template("studentPage.html", things=rows)
    else:
        return render_template("studentPage.html", things=rows)
    

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

@app.route("/studentNotes", methods=["POST", "GET"])
def studentNotes():
    if request.method == "POST":
        studentNotes = func.viewStudentNotes() # calls viewStudentNotes
        return render_template("studentNotes.html", things=studentNotes) #passes studentNotes to page 'studentNotes.html' to have it's contents printed to screen
    studentNotes = func.viewStudentNotes() # calls viewStudentNotes
    return render_template("studentNotes.html", things=studentNotes)
    if request.method == "POST":
        if 'ViewNotes' in request.form:
            studentNotes = func.viewStudentNotes()
            return render_template("studentNotes.html", things=studentNotes)
        else:
            studentNotes = func.viewStudentNotes()
            return render_template("studentNotes.html", things=studentNotes)
    else:
        studentNotes = func.viewStudentNotes()
        return render_template("studentNotes.html", things=studentNotes)



if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()

#Am I gonna have to keep track of the noteID somewhere