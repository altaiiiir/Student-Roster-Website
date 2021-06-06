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
cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_Catalog.ID, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
FROM Transcript
	JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
	JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)
	JOIN Student ON (Transcript.StudentID = Student.ID)""")
transcriptRows = cur.fetchall()

findMaxNoteID = """Select MAX(NoteID) from Student_Notes"""
cur.execute(findMaxNoteID)
maxNotInForm = cur.fetchall()
max = maxNotInForm[0][0] #get max note because idk how we are keeping track of noteID
#print(max)

#func.viewAdmin()

cur.execute("""select * from Note""")
notesRows = cur.fetchall()
#print(notesRows)

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/") 
def home():
    return render_template("index.html", things=rows)

@app.route("/studentPage", methods=["POST", "GET"]) 
def studentPage():
    if request.method == "POST":

        studentNotes = func.viewStudentNotes()
        if 'viewNotes' in request.form:
            print("clicked viewNotes")
            return render_template('studentNotes.html', things = studentNotes) #renders studentNotes page
        elif 'viewStudentName' in request.form:
            theStudentID = request.form["theirID"]
            specificStudent = "Select * from Student where Student.StudentID = %s" 
            if (theStudentID != ""):
                cur.execute(specificStudent, (theStudentID,)) # view the student based on their firstName and id
                specificStudent = cur.fetchall()
                return render_template("studentPage.html", things=specificStudent)
            else:
                return render_template("studentPage.html", things=rows) #returns query of that user and studentID to studentPage

        return render_template("studentPage.html", things=rows) #returns query of that user and studentID to studentPage
        #I need to add a studentNoteInput.html page that asks user for the Note, and the type 
        
    return render_template("studentPage.html", things=rows)
    
@app.route("/studentNotes", methods=["POST", "GET"])
def studentNotes():
    studentNotes = func.viewStudentNotes()
    if request.method == "POST":
        studentNotes = func.viewStudentNotes()
        if 'delete' in request.form:
            print ("DELETE WAS RANNNN")
            theStudentID = request.form["theirID"]
            note = request.form["notes"]
            noteType = request.form["noteType"]
            theNoteID = request.form["NoteID"]
            if (theNoteID == ""):
                return render_template("studentNotes.html", things=studentNotes)

            noteQuery = """ delete from note where note.noteID = %s """
            getSerial = """select ID from note where NoteID = %s """
            cur.execute(getSerial, (theNoteID,))
            NoteSerialNotInForm= cur.fetchall()
            noteSerialInForm = NoteSerialNotInForm[0][0]
          
            student_notesQuery = """ delete from Student_Notes where student_notes.StudentID = %s AND student_notes.noteID = %s """
            cur.execute(student_notesQuery, (theStudentID, noteSerialInForm))
            con.commit()
            cur.execute(noteQuery, (theNoteID,))
            con.commit()
            studentNotes = func.viewStudentNotes() # calls viewStudentNotes
            return render_template("studentNotes.html", things=studentNotes) #passes studentNotes to page 'studentNotes.html' to have it's contents printed to screen
        elif 'add' in request.form:
            print ("WENT THROUGH ADD")
            theStudentID = request.form["theirID"]
            note = request.form["notes"]
            noteType = request.form["noteType"]
            #theNoteID = request.form["NoteID"]
            if theStudentID == "" or note =="":
                return render_template("studentNotes.html", things=studentNotes)
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
            studentNotesInsert = """INSERT INTO Student_Notes (NoteID, StudentID) Values (%s, %s)"""
            
            #print(max, note, currentDate, noteType, adminID )
            cur.execute(studentInsert, (max, note, currentDate, noteType, adminID )) #here trying to insert the studentID and notID into the student_notes table 
            con.commit()
            getSerial = """SELECT Note.ID from Note where Note.NoteID = %s"""
            cur.execute(getSerial, (max,))
            theSerial = cur.fetchall()
            serialRightForm = theSerial[0][0]

            cur.execute(studentNotesInsert,(serialRightForm, theStudentID))
            con.commit()
            badquery = """SELECT Student_Notes.StudentID, Note.NoteID, Student.FirstName, Student.LastName,
                                 Note.Note, Note.Date, Note.Type, Note_Type.Name FROM Student_Notes
                   JOIN Note ON (Student_Notes.NoteID = Note.ID)
                   JOIN Note_Type ON (Note.Type = Note_Type.Type)
                   JOIN Student ON (Student_Notes.StudentID = Student.ID)
                    """
            query = """select * from Note"""
            cur.execute(badquery)
            studentNotesRows = cur.fetchall()
            #print(studentNotesRows)
            studentNotes = func.viewStudentNotes()
            allStudents = func.viewAllStudents()
            return render_template("studentNotes.html", things=studentNotes)
        print ("post")
        studentNotes = func.viewStudentNotes() # calls viewStudentNotes
        return render_template("studentNotes.html", things=studentNotes)
    print ("no post")
    studentNotes = func.viewStudentNotes() # calls viewStudentNotes
    return render_template("studentNotes.html", things=studentNotes)
    

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





if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()

#Am I gonna have to keep track of the noteID somewhere