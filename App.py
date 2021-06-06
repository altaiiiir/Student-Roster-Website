from re import split
import psycopg2
from flask import Flask, redirect, url_for, render_template, request, session, flash

import func
from datetime import timedelta, datetime
import datetime
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

@app.route("/view-student")
def viewStudent():
    cur.execute('Select * from Student')
    rows = cur.fetchall()
    return render_template("StudentPage.html", things=rows)

@app.route("/transcript-filter", methods=["POST", "GET"])
def TranscriptFilter():
   if 'filterAll' in request.form:
      try:
         studentID = int(request.form["studentID"])
      except:
         flash("Invalid Number Entry", "info")
         return render_template("filterTranscript.html")

      cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                        FROM Transcript
                           JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                           JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                           JOIN Student ON (Transcript.StudentID = Student.ID)
                        WHERE student.id = %s""", [studentID])
      updatedTranscriptRows = cur.fetchall()
      return render_template("Transcripts.html", things=updatedTranscriptRows)
   elif 'filterCur' in request.form:
      try:
         studentID = int(request.form["studentID"])
      except:
         flash("Invalid Number Entry", "info")
         return render_template("filterTranscript.html")
      cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                        FROM Transcript
                           JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                           JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                           JOIN Student ON (Transcript.StudentID = Student.ID)
                        WHERE student.id = %s AND transcript.finalGrade IS NULL""", [studentID])
      updatedTranscriptRows = cur.fetchall()
      return render_template("Transcripts.html", things=updatedTranscriptRows)
   elif 'filterCor' in request.form:
      try:
         SLN = int(request.form["SLN"])
      except:
         flash("Invalid Number Entry", "info")
         return render_template("filterTranscript.html")
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

@app.route("/transcript-add-remove", methods=["POST", "GET"])
def TranscriptAddRemove():
   if request.method == "POST":
      studentID = request.form["studentID"]
      if studentID == '':
         flash("Enter In Student ID", "info")
         return render_template("TranscriptAddRemove.html")
      SLN = request.form["SLN"]
      if SLN == '':
         flash("Enter in SLN", "info")
         return render_template("TranscriptAddRemove.html")
      cur.execute('SELECT ID FROM Course_Info WHERE SLN = %s', [SLN])
      classIDs = cur.fetchall()
      if classIDs.__len__() == 0:
         flash("Class Doesn't Exist", "info")
         return render_template("TranscriptAddRemove.html")
      classID = classIDs[0][0]
      if 'delete' in request.form:
         cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',(studentID, classID))
         isConnection = cur.fetchall()
         if isConnection.__len__() == 0:
            flash("Student is not Enrolled in the Class", "info")
            return render_template("TranscriptAddRemove.html")
         cur.execute('''DELETE FROM Transcript WHERE classID = %s AND studentID = %s''', (int(classID), studentID))
      elif 'addStudent' in request.form:
         try:
            grade = request.form["grade"]
         except:
            grade = ''
         #adds either a grade with null or with a final grade
         if grade == '':
            cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',(studentID, classID))
            isConnection = cur.fetchall()
            if isConnection.__len__() == 0:
               cur.execute('''INSERT INTO Transcript (StudentID, ClassID)
                  Values(%s, %s)''', (studentID, int(classID)))
            else:
               flash("Student is Already in the Class", "info")
               return render_template("TranscriptAddRemove.html")
      else:
         grade = request.form["grade"]
         if grade == '':
            flash("Enter Grade", "info")
            return render_template("TranscriptAddRemove.html")
         #adding grade
         cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',(studentID, classID))
         isConnection = cur.fetchall()
         if isConnection.__len__() == 0:
            flash("Student is not Enrolled in the Class", "info")
            return render_template("TranscriptAddRemove.html")
         else:
            if float(grade) < 0.0 or float(grade) > 4.0:
               flash("Not a valid grade", "info")
               return render_template("TranscriptAddRemove.html")
            cur.execute('''UPDATE Transcript SET 
               finalGrade = %s WHERE studentID = %s AND classID = %s''', (grade, studentID, int(classID)))
      con.commit()
      return redirect(url_for("Transcript"))
   else:        
      return render_template("TranscriptAddRemove.html")

@app.route("/transcript", methods=["POST", "GET"])
def Transcript():
    cur.execute("""SELECT Student.ID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                    FROM Transcript
                        JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                        JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                        JOIN Student ON (Transcript.StudentID = Student.ID)
                  ORDER BY Student.ID""")
    updatedTranscriptRows = cur.fetchall()
    return render_template("Transcripts.html", things=updatedTranscriptRows)


@app.route("/add-remove-student", methods = ["POST","GET"])
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

@app.route("/class-info")
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

@app.route("/add-course", methods = ["POST", "GET"])
def add():
    if request.method == "POST":

        # check if its an add or remove
        if 'add' in request.form:
            # request data
            name = request.form["nm"]
            cc = request.form["creds"]
            type = request.form["type"]

            if(name and cc and type) :
                # checks if course already exists
                cur.execute('Select * from Course_Catalog')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]
                
                    if (curName == name): 
                        flash("You cannot add a course that already exists.", "error") 
                        return render_template("addCourse.html")

                # ---------------
                # adds to course catalog
                cur.execute("""INSERT INTO Course_Catalog (Name, CourseCredits, Type) 
                                VALUES (%s, %s, %s)""", (name, cc, type))

                # update table
                cur.execute('Select * from Course_Catalog')
                courseRows = cur.fetchall()
                con.commit()

                return render_template("CourseCatalog.html", things = courseRows)
            else:
                flash("Fill in neccesary information.") 
                return render_template("addCourse.html")
        else:
            name = request.form["nm"]
            if(name) :
                # checks if course doesn't exist
                cur.execute('Select * from Course_Catalog')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]
                
                    if (curName == name): 
                        courseExist = 1 # true
                    # removes course from course catalog
                        cur.execute("""DELETE FROM Course_Catalog WHERE Name = %s""", [name])
                        con.commit()

                        # update table
                        cur.execute('Select * from Course_Catalog')
                        courseRows = cur.fetchall()
                        
                        return render_template("CourseCatalog.html", things = courseRows) 
                    else:
                        courseExist = 0 # false
                        
                if (courseExist == 0):
                    flash("You cannot remove a course that doesn't exists.", "error") 
                    return render_template("addCourse.html")
            else:
                flash("Fill in neccesary information.") 
                return render_template("addCourse.html")
    else:
        return render_template("addCourse.html")

@app.route("/add-class", methods = ["POST", "GET"])
def addClass():
    if request.method == "POST":

        # check if its an add or remove
        if 'add' in request.form:
            # request data
            name = request.form["name"]
            section = request.form["section"]
            roomid = request.form["roomid"]
            instructor = request.form["ins"]
            time = request.form["time"]
            quarter = request.form["quarter"]
            year = request.form["yr"]

            if(name and section and roomid and instructor and time and quarter and year) :
                # error flags
                existsInCatalog = 0 # false
                roomExists = 0 # false
                roomHasSpace = 0 # false
                roomAvaliable = 1 # true

                # checks for room time avaliability 
                cur.execute('SELECT * FROM Course_Info WHERE RoomID = %s', [roomid])
                tempRows = cur.fetchall()
                for x in tempRows:
                    curTime = x[6]
                    tempCurTime = curTime.strftime("%H:%M:%S")
                    tempTime = time + ':00'
                    if (tempCurTime == tempTime):
                        roomAvaliable = 0 # false

                # checks for room space and existence 
                cur.execute('SELECT * FROM Classroom')
                tempRows = cur.fetchall()
                for x in tempRows:
                    curRoom = x[2]
                    
                    curCapacity = x[3]
                    if (int(curRoom) == int(roomid)):
                        roomExists = 1 # true
                    if (int(curCapacity) >= int(curCapacity+1)):
                        roomHasSpace = 1 # true

                # checks for class existance in course
                cur.execute('SELECT * FROM Course_Catalog')
                tempRows = cur.fetchall()
                for x in tempRows:
                    curName = x[1]
                    if (curName == name):
                        existsInCatalog = 1 # true

                # checks for duplicate class
                cur.execute('Select * from Course_Catalog JOIN Course_Info ON (Course_Catalog.ID = Course_Info.CourseID)')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]
                    curSection = r[7]

                    if (curName == name and curSection == section): 
                        flash("You cannot add a class that already exists.") 
                        return render_template("addClass.html")

                # Case: class time conflict
                if roomAvaliable == 0:
                    flash("Time conflict within that building.") 
                    return render_template("addClass.html")

                # Case: class not in catalog
                if existsInCatalog == 0:
                    flash("You cannot add a class to a course that doesn't exist.") 
                    return render_template("addClass.html")

                # Case: room doesn't exist
                if roomExists == 0:
                    flash("You cannot add a class to a room that doesn't exist.") 
                    return render_template("addClass.html")

                # Case: room is full
                if roomHasSpace == 0:
                    flash("You cannot add a class to a full room.") 
                    return render_template("addClass.html")    
                
                # adds to course info
                cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [name])
                idEntry = cur.fetchall()
                id = idEntry[0][0]
                
                cur.execute("""INSERT INTO Course_Info (CourseID, Section, RoomID, InstructorName, Time, Quarter, Year) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""", (id, section, roomid, instructor, time, quarter, year))

                con.commit()

                # update table
                cur.execute('Select * from Course_Info')
                courseInfoRows = cur.fetchall()
                con.commit()

                return render_template("courseInfo.html", things=showCourseInfoRows())
            else:
                flash("Fill in neccesary information.") 
                return render_template("addClass.html")    
        else:
            # request data
            name = request.form["name"]
            section = request.form["section"]

            if(name and section) :
                # for class delete only name and section are needed
                # checks if class doesn't exist in course_Info 
                cur.execute('Select * from Course_Catalog JOIN Course_Info ON (Course_Catalog.ID = Course_Info.CourseID)')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]
                    curSection = r[7]

                    if (curName == name and curSection == section): 
                        courseExist = 1 # true
                        cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [name])
                        idEntry = cur.fetchall()
                        id = idEntry[0][0]

                        cur.execute('SELECT SLN FROM Course_Info WHERE CourseID = %s AND Section = %s', (id, section))
                        slnEntry = cur.fetchall()
                        sln = slnEntry[0][0]

                        # removes course from course Info
                        cur.execute("""DELETE FROM Course_Info WHERE SLN = %s""", [sln])
                        con.commit()

                        # update table
                        cur.execute('Select * from Course_Info')
                        courseInfoRows = cur.fetchall()
                
                        return render_template("courseInfo.html", things=showCourseInfoRows())
                    else:
                        courseExist = 0 # false
                        
                if (courseExist == 0):
                    flash("You cannot remove a class that doesn't exists.", "error") 
                    return render_template("addClass.html")
            else:
                flash("Fill in neccesary information.") 
                return render_template("addClass.html")
    else:
        # show main screen initially
        return render_template("addClass.html")

@app.route("/view-student-notes", methods = ["POST", "GET"])
def viewStudentNotes():
    studentNotes = func.viewStudentNotes()
    if request.method == "POST":
        
        if 'modifyNotes' in request.form:
            
            studentNotes = func.viewStudentNotes()
            return render_template('modifyStudentNotes.html', things = studentNotes)
        
        if 'viewNotes' in request.form:
            theStudentID = request.form["theirID"]
               
            if (theStudentID != ""):
                    
                if (theStudentID.isdecimal() == 0):
                    flash("StudentID must be a number", "error")
                    return render_template("viewStudentNotes.html", things=studentNotes)

                specificStudent = func.viewSpecificStudentNotes(theStudentID)
                return render_template("viewStudentNotes.html", things=specificStudent)
            else:
                return render_template("viewStudentNotes.html", things=studentNotes)
    
    studentNotes = func.viewStudentNotes()
    return render_template("viewStudentNotes.html", things=studentNotes)

@app.route("/modify-student-notes", methods=["POST", "GET"])
def modifyStudentNotes():
    studentNotes = func.viewStudentNotes()
    if request.method == "POST":
        if 'viewNotes' in request.form:
            print("clicked viewNotes")
            studentNotes = func.viewStudentNotes()
            return render_template('viewStudentNotes.html')
        
        if 'delete' in request.form:
            print ("DELETE WAS RANNNN")
            theStudentID = request.form["theirID"]
            note = request.form["notes"]
            noteType = request.form["noteType"]
            theNoteID = request.form["NoteID"]
            theDate = request.form["date"]
           
            if (theNoteID.isdecimal() == 0 or theStudentID.isdecimal() == 0):
                flash("Please enter a valid NoteID and StudentID", "error")
                return render_template("modifyStudentNotes.html", things = studentNotes)

            print ("after first if")
            doesNoteExist = """ select * from Note where NoteID = %s; """
            
            doesStudentHaveBoth = """select * from student_notes where studentID = %s; """ 
            
            allRowsStudentNotes = """select * from student_notes """
            isStudentLinkedWithNote = """select StudentID, Student_notes.NoteID, Note.NoteID from student_notes
                                         JOIN Note ON (student_notes.noteID = Note.ID)   
                                         where studentID = %s AND Note.NoteID = %s;  """
            
            cur.execute(isStudentLinkedWithNote, (theStudentID, theNoteID))
            linkedwithnotequery= cur.fetchall()

            linkedstud = 0
            linkednote = 0
            for x in linkedwithnotequery:
                studid = x[0]
                noteid = x[2]
                if (str(studid) == theStudentID):
                    linkedstud =1
                if (str(noteid) == theNoteID):
                    linkednote = 1
            if (linkedstud == 0 or linkednote == 0):
                flash("Please enter a valid NoteID and StudentID combination", "error")
                return render_template("modifyStudentNotes.html", things = studentNotes)

            cur.execute(allRowsStudentNotes)
            allRowsQuery= cur.fetchall()
            print(allRowsQuery)

            cur.execute(doesStudentHaveBoth, (theStudentID,))
            studentIDExists = 0
            NoteIDExists = 0
            tempRows = cur.fetchall() #does studentid exist
            print (tempRows)
            
            for x in tempRows:
                curStudID = x[0]
                if (str(curStudID) == theStudentID):
                    studentIDExists = 1 # true
                    print("student id exists")
            
            cur.execute(doesNoteExist, (theNoteID,))
            noteQuery = cur.fetchall()
            print (noteQuery)
            for r in noteQuery:
                curNotID = r[1]
                if (str(curNotID) == theNoteID):
                    NoteIDExists = 1
                    print("note id exists")
           
            if (studentIDExists == 0 or NoteIDExists == 0):
                flash("Please enter a valid NoteID and StudentID", "error")
                return render_template("modifyStudentNotes.html", things = studentNotes)

        

            noteQuery = """ delete from note where note.noteID = %s """
            getSerial = """select ID from note where NoteID = %s """
            cur.execute(getSerial, (theNoteID,))
            NoteSerialNotInForm= cur.fetchall()
            noteSerialInForm = NoteSerialNotInForm[0][0]
          
            student_notesQuery = """ delete from Student_Notes where student_notes.StudentID = %s AND student_notes.noteID = %s; """
            cur.execute(student_notesQuery, (theStudentID, noteSerialInForm))
            con.commit()
            cur.execute(noteQuery, (theNoteID,))
            con.commit()
            studentNotes = func.viewStudentNotes() # calls viewStudentNotes
            flash("Successfully deleted note")
            return render_template("modifyStudentNotes.html") #passes studentNotes to page 'studentNotes.html' to have it's contents printed to screen
      
      
        elif 'add' in request.form:
            print ("WENT THROUGH ADD")
            theStudentID = request.form["theirID"]
            note = request.form["notes"]
            noteType = request.form["noteType"]
            theDate = request.form["date"]
            if theStudentID == "" or note == "" or theDate == "":
                flash("Please enter a valid StudentID, note and date", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)
            
            splitDate = theDate.split("/")
            if len(splitDate) != 3:
                flash("Please enter a valid date", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)
            month = splitDate[0]
            day = splitDate[1]
            year = splitDate[2]
            
            if (month.isdecimal() == 0 or day.isdecimal() == 0 or year.isdecimal() == 0 ):
                flash("Please enter a valid date", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)
            month = int(splitDate[0])
            day = int(splitDate[1])
            year = int(splitDate[2])

            if(month > 12 or month < 1):
                flash("Please enter a valid date", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)
            if(day > 31 or day < 1):
                flash("Please enter a valid date", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)
            if(year > 2021 or year < 1):
                flash("Please enter a valid date", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)

            dateObject = datetime.datetime(year, month, day)
            curDate = date.today()

            if (dateObject > datetime.datetime.now()):
                flash("Please enter a date that is prior to today", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)
            print (dateObject)
            print(date.today())
            #theNoteID = request.form["NoteID"]
            
            if (theStudentID.isdecimal() == 0):
                flash("Please enter a valid StudentID", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)
            
            studentQuery = """select * from student where ID = %s; """
            cur.execute(studentQuery, (theStudentID,)) 
           
            studentQueryResult = cur.fetchall()
            print (studentQueryResult)
            studentIDExists = 0
            for x in studentQueryResult:
                curStudID = x[0]
                
                print(type(theStudentID))
                if (str(curStudID) == theStudentID):
                    studentIDExists = 1 # true
                    print ("went thorought checks ")
            print (studentIDExists)
            if (studentIDExists == 0):
                flash("Please enter a valid StudentID", "error")
                return render_template("modifyStudentNotes.html", things=studentNotes)    
            print ("went thorought checks ")

            findMaxNoteID = """Select MAX(NoteID) from Note""" #find max note from Note  
            cur.execute(findMaxNoteID)
            maxNotInForm = cur.fetchall()
            max = maxNotInForm[0][0] #get max note because idk how we are keeping track of noteID
            max = max + 1
            adminID = 1
            currentDate = date.today()
            studentInsert = """INSERT INTO Note (NoteID, Note, Date, Type, AdminID)
                                Values(%s, %s, %s, %s, %s);""" #OKAY so apparently I need to insert into Note first and then connect that to Student Notes
                                                  #by creating the note and then saying "insert into student_Notes where the Student_Notes.NoteID == Note.ID (the note that I just created in the Note table"  
            studentNotesInsert = """INSERT INTO Student_Notes (NoteID, StudentID) Values (%s, %s);"""
            
            #print(max, note, currentDate, noteType, adminID )
            
            cur.execute(studentInsert, (max, note, dateObject, noteType, adminID )) #here trying to insert the studentID and notID into the student_notes table 
            con.commit()
            getSerial = """SELECT Note.ID from Note where Note.NoteID = %s;"""
            cur.execute(getSerial, (max,))
            theSerial = cur.fetchall()
            serialRightForm = theSerial[0][0]

            cur.execute(studentNotesInsert,(serialRightForm, theStudentID))
            con.commit()
            badquery = """SELECT Student_Notes.StudentID, Note.NoteID, Student.FirstName, Student.LastName,
                                 Note.Note, Note.Date, Note.Type, Note_Type.Name FROM Student_Notes
                   JOIN Note ON (Student_Notes.NoteID = Note.ID)
                   JOIN Note_Type ON (Note.Type = Note_Type.Type)
                   JOIN Student ON (Student_Notes.StudentID = Student.ID);
                    """
            query = """select * from Note"""
            cur.execute(badquery)
            studentNotesRows = cur.fetchall()
            #print(studentNotesRows)
            studentNotes = func.viewStudentNotes()
            allStudents = func.viewAllStudents()
            return render_template("modifyStudentNotes.html", things=studentNotes)
        print ("post")
        studentNotes = func.viewStudentNotes() # calls viewStudentNotes
        return render_template("modifyStudentNotes.html", things=studentNotes)
    print ("no post")
    studentNotes = func.viewStudentNotes() # calls viewStudentNotes
    return render_template("modifyStudentNotes.html", things=studentNotes)
    

if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()
