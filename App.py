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

def showCourseInfoRows():
    cur.execute(
        'Select * from Course_Info '
        '   JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)'
        'ORDER BY Course_Catalog.Name')
    courseInfoRows = cur.fetchall()
    return courseInfoRows

cur.execute(
    'SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)'
    '   JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) '
    '   JOIN Student ON (Student.ID = Transcript.StudentID) '
    'WHERE Course_Info.CourseID = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

#execute query
cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)')
courseInfoRows = cur.fetchall()

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/viewStudent") 
def viewStudent():
    cur.execute('Select * from Student')
    rows = cur.fetchall()
    return render_template("studentPage.html", things=rows)

@app.route("/TranscriptFilter", methods=["POST", "GET"])
def TranscriptFilter():
   if 'filterAll' in request.form:
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
      return render_template("filterTranscript.html")

@app.route("/TranscriptAddRemove", methods=["POST", "GET"])
def TranscriptAddRemove():
   if request.method == "POST":
      studentID = request.form["studentID"]
      SLN = request.form["SLN"]
      cur.execute('SELECT ID FROM Course_Info WHERE SLN = %s', [SLN])
      classIDs = cur.fetchall()
      if classIDs.__len__() == 0:
         flash("Class Doesn't Exist", "info")
         return render_template("Transcriptaddremove.html")
      classID = classIDs[0][0]
      if 'delete' in request.form:
         cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',(studentID, classID))
         isConnection = cur.fetchall()
         if isConnection.__len__() == 0:
            flash("Student is not Enrolled in the Class", "info")
            return render_template("Transcriptaddremove.html")
         cur.execute('''DELETE FROM Transcript WHERE classID = %s AND studentID = %s''', (int(classID), studentID))
      elif 'addStudent':
         grade = request.form["grade"]
         #adds either a grade with null or with a final grade
         if grade == '':
            cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',(studentID, classID))
            isConnection = cur.fetchall()
            if isConnection.__len__() == 0:
               cur.execute('''INSERT INTO Transcript (StudentID, ClassID)
                  Values(%s, %s)''', (studentID, int(classID)))
            else:
               flash("Student is Already in the Class", "info")
               return render_template("Transcriptaddremove.html")
         else:
            #adding grade
            cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',(studentID, classID))
            isConnection = cur.fetchall()
            if isConnection.__len__() == 0:
               flash("Student is not Enrolled in the Class", "info")
               return render_template("Transcriptaddremove.html")
            else:
               if float(grade) < 0.0 or float(grade) > 4.0:
                  flash("Not a valid grade", "info")
                  return render_template("Transcriptaddremove.html")
               cur.execute('''UPDATE Transcript SET 
                  finalGrade = %s WHERE studentID = %s AND classID = %s''', (grade, studentID, int(classID)))
      con.commit()
      return redirect(url_for("Transcript"))
   else:        
      return render_template("Transcriptaddremove.html") 

@app.route("/Transcript", methods=["POST", "GET"])
def Transcript():
    cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                    FROM Transcript
                        JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                        JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                        JOIN Student ON (Transcript.StudentID = Student.ID)
                  ORDER BY Student.ID""")
    updatedTranscriptRows = cur.fetchall()
    return render_template("Transcripts.html", things=updatedTranscriptRows)


@app.route("/addRemoveStudent", methods = ["POST","GET"]) 
def addRemoveStudent():
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
    else:
        return render_template("addRemoveStudent.html")

@app.route("/course-catalog", methods=["POST", "GET"])
def courses_catalog():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        cur.execute('Select * from Course_Catalog')
        courseRows = cur.fetchall()
        return render_template("CourseCatalog.html", things=courseRows)

@app.route("/course-info")
def course_info():
    return render_template("CourseInfo.html", things=showCourseInfoRows())

@app.route("/update-class", methods=["POST", "GET"])
def update_course():
    if request.method == "POST":
        currSln = request.form["sln"]
        newCourseName = request.form["CourseName"]
        newSection = request.form["Section"]
        newRoomID = request.form["RoomID"]
        newInstructorName = request.form["InstructorName"]
        newTime = request.form["Time"]
        newQuarter = request.form["Quarter"]
        newYear = request.form["Year"]

        if newCourseName is not "":
            cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [newCourseName])
            tempCourseID = cur.fetchall()
            newCourseID = tempCourseID[0][0]
            cur.execute('UPDATE Course_Info SET CourseID = %s WHERE sln = %s', (newCourseID, currSln))

        if newSection is not "":
            cur.execute('UPDATE Course_Info SET Section = %s WHERE sln = %s', (newSection, currSln))

        if newRoomID is not "":
            cur.execute('UPDATE Course_Info SET RoomID = %s WHERE sln = %s', (newRoomID, currSln))

        if newInstructorName is not "":
            cur.execute('UPDATE Course_Info SET InstructorName = %s WHERE sln = %s', (newInstructorName, currSln))

        if newTime is not "":
            cur.execute('UPDATE Course_Info SET Time = %s WHERE sln = %s', (newTime, currSln))

        if newQuarter is not "":
            cur.execute('UPDATE Course_Info SET Quarter = %s WHERE sln = %s', (newQuarter, currSln))

        if newYear is not "":
            cur.execute('UPDATE Course_Info SET Year = %s WHERE sln = %s', (newYear, currSln))

        con.commit()
        return render_template("CourseInfo.html", things=showCourseInfoRows())
    else:
        return render_template("UpdateClass.html")

if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()
