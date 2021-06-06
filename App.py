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

@app.route("/addCourse", methods = ["POST", "GET"])
def add():
    if request.method == "POST":

        # request data
        name = request.form["nm"]
        cc = request.form["creds"]
        type = request.form["type"]

        # check if its an add or remove
        if 'add' in request.form:

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
        return render_template("addCourse.html")

@app.route("/addClass", methods = ["POST", "GET"])
def addClass():
    if request.method == "POST":

        # request data
        name = request.form["name"]
        section = request.form["section"]
        roomid = request.form["roomid"]
        instructor = request.form["ins"]
        time = request.form["time"]
        quarter = request.form["quarter"]
        year = request.form["yr"]

        # check if its an add or remove
        if 'add' in request.form:
        
            # error flags
            existsInCatalog = 0 # false
            roomExists = 0 # false
            roomHasSpace = 0 # false

            # checks for room space and existence 
            cur.execute('SELECT * FROM Classroom')
            tempRows = cur.fetchall()
            for x in tempRows:
                curRoom = x[2]
                curCapacity = x[3]
                if (curRoom == roomid):
                    roomExists = 1 # true
                if (curCapacity >= curCapacity+1):
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
        # show main screen initially
        return render_template("addClass.html")

if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()
