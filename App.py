from re import split
import psycopg2
from flask import Flask, redirect, url_for, render_template, request, session, flash, g

import func
from datetime import timedelta, datetime
import datetime
from datetime import date

today = date.today()
print("Today's date:", today)

# connect to the local host db
con = psycopg2.connect(
    host="database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
    database="webdb",
    user="postgres",
    password="2fD9vPoMU6HAfMM"
)

# cursor
cur = con.cursor()


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='admin', password='admin'))


def showCourseInfoRows():
    cur.execute('SELECT Course_Info.ID, Course_Info.SLN, Course_Catalog.name, Course_Info.Section,  '
                ' Course_Info.RoomID, Course_Info.Instructorname, Course_Info.Time, Course_Info.Quarter,'
                ' Course_Info.Year, COUNT (Transcript) AS butsinseat, Classroom.Capacity'
                ' FROM Course_INFO '
                '   LEFT JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) '
                '   RIGHT JOIN Classroom ON (Course_Info.RoomID = Classroom.ID)'
                'Join Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)'
                'GROUP BY Course_Info.ID, Classroom.ID, Course_Catalog.ID ORDER BY Course_Info.SLN')
    courseInfoRows = cur.fetchall()
    return courseInfoRows


def showCourseCatalogRows():
    cur.execute('Select * from Course_Catalog ORDER BY Course_Catalog.Name')
    courseRows = cur.fetchall()
    return courseRows


cur.execute(
    'SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)'
    '   JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) '
    '   JOIN Student ON (Student.ID = Transcript.StudentID) '
    'WHERE Course_Info.CourseID = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

# execute query
cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)')
courseInfoRows = cur.fetchall()

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def login():
    session.pop('user_id', None)
    print(users)
    u1 = getattr(users[0], 'username')
    p1 = getattr(users[0], 'password')
    id1 = getattr(users[0], 'id')
    if request.method == 'POST':
        # session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        if (username == "" or password == ""):
            flash("Enter valid username and password", "error")
            return render_template('Login.html')

        if (u1 != username or p1 != password):
            flash("Enter valid username and password", "error")
            return redirect(url_for('login'))

        session['user_id'] = id1
        return redirect(url_for('home'))

    return render_template('Login.html')


@app.route("/Index.html")
def home():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("Index.html")


@app.route("/view-student")
def viewStudent():
    if not g.user:
        return redirect(url_for('login'))
    cur.execute('Select * from Student ORDER BY Student.StudentID')
    rows = cur.fetchall()
    return render_template("StudentPage.html", things=rows)


@app.route("/transcript-filter", methods=["POST", "GET"])
def TranscriptFilter():
    if not g.user:
        return redirect(url_for('login'))
    if 'filterAll' in request.form:
        try:
            studentID = int(request.form["studentID"])
        except:
            flash("Invalid Number Entry", "info")
            return render_template("FilterTranscript.html")

        cur.execute("""SELECT Student.StudentID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                        FROM Transcript
                           JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                           JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                           JOIN Student ON (Transcript.StudentID = Student.ID)
                        WHERE student.Studentid = %s
                        ORDER BY Course_Catalog.name""", [studentID])
        updatedTranscriptRows = cur.fetchall()
        return render_template("Transcripts.html", things=updatedTranscriptRows)
    elif 'filterCur' in request.form:
        try:
            studentID = int(request.form["studentID"])
        except:
            flash("Invalid Number Entry", "info")
            return render_template("FilterTranscript.html")
        cur.execute("""SELECT Student.StudentID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                        FROM Transcript
                           JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                           JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                           JOIN Student ON (Transcript.StudentID = Student.ID)
                        WHERE student.StudentID = %s AND transcript.finalGrade IS NULL
                        ORDER BY Course_Catalog.name""", [studentID])
        updatedTranscriptRows = cur.fetchall()
        return render_template("Transcripts.html", things=updatedTranscriptRows)
    elif 'filterCor' in request.form:
        try:
            SLN = int(request.form["SLN"])
        except:
            flash("Invalid Number Entry", "info")
            return render_template("FilterTranscript.html")
        cur.execute("""SELECT Student.StudentID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                        FROM Transcript
                           JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                           JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                           JOIN Student ON (Transcript.StudentID = Student.ID)
                        WHERE course_info.SLN = %s
                        ORDER BY Student.LastName""", [SLN])
        updatedTranscriptRows = cur.fetchall()
        return render_template("Transcripts.html", things=updatedTranscriptRows)
    else:
        return render_template("FilterTranscript.html")


@app.route("/transcript-add-remove", methods=["POST", "GET"])
def TranscriptAddRemove():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "POST":
        studentID = request.form["studentID"]
        try:
            studentID = int(studentID)
        except:
            flash("Enter in ID", "info")
            return render_template("TranscriptAddRemove.html")
        if studentID == '':
            flash("Enter In Student ID", "info")
            return render_template("TranscriptAddRemove.html")

        sln = request.form["SLN"]
        sln = sln
        if sln == '':
            flash("Enter in SLN", "info")
            return render_template("TranscriptAddRemove.html")
        cur.execute('SELECT ID FROM Course_Info WHERE SLN = %s', [int(sln)])
        classIDs = cur.fetchall()
        if classIDs.__len__() == 0:
            flash("Class Doesn't Exist", "info")
            return render_template("TranscriptAddRemove.html")
        classID = classIDs[0][0]
        if 'delete' in request.form:
            cur.execute('''SELECT id FROM Student WHERE studentid = %s''', [studentID])
            curStud = cur.fetchall()
            if curStud.__len__() != 0:
                curStud = curStud[0][0]
            else:
                flash("Student doesn't Exist", "info")
                return render_template("TranscriptAddRemove.html")
            cur.execute('''SELECT StudentID FROM Transcript WHERE studentid = %s AND classID = %s''',
                        (curStud, classID))
            isConnection = cur.fetchall()
            if isConnection.__len__() == 0:
                flash("Student is not enrolled in the Class", "info")
                return render_template("TranscriptAddRemove.html")
            cur.execute('''DELETE FROM Transcript WHERE classID = %s AND studentID = %s''', (int(classID), curStud))
            con.commit()
        elif 'addStudent' in request.form:
            try:
                grade = request.form["grade"]
            except:
                grade = ''
            # adds either a grade with null or with a final grade
            if grade == '':
                cur.execute('''SELECT id FROM Student WHERE studentid = %s''', [studentID])
                curStud = cur.fetchall()
                curStud = curStud[0][0]
                cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',
                            (curStud, classID))
                isConnection = cur.fetchall()
                if isConnection.__len__() == 0:
                    cur.execute('''INSERT INTO Transcript (StudentID, ClassID)
                  Values(%s, %s)''', (curStud, int(classID)))
                else:
                    flash("Student is Already in the Class.", "info")
                    return render_template("TranscriptAddRemove.html")
        else:
            grade = request.form["grade"]
            if grade == '':
                flash("Enter Grade", "info")
                return render_template("TranscriptAddRemove.html")
            # adding grade
            
            cur.execute('''SELECT id FROM Student WHERE studentid = %s''', [studentID])
            curStud = cur.fetchall()
            if curStud.__len__() != 0:
                curStud = curStud[0][0]
            else:
                flash("Student doesn't Exist", "info")
                return render_template("TranscriptAddRemove.html")

            cur.execute('''SELECT studentID FROM Transcript WHERE studentid = %s AND classID = %s''',
               (curStud, int(classID)))
            isConnection = cur.fetchall()

            if isConnection.__len__() == 0:
                flash("Student doesn't exist in class.", "info")
                return render_template("TranscriptAddRemove.html")
            else:
                if float(grade) < 0.0 or float(grade) > 4.0:
                    flash("Not a valid grade", "info")
                    return render_template("TranscriptAddRemove.html")
                cur.execute('''UPDATE Transcript SET 
               finalGrade = %s WHERE studentID = %s AND classID = %s''', (grade, curStud, int(classID)))
        
        con.commit()
        cur.execute("""SELECT Student.StudentID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                                FROM Transcript
                                   JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                                   JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                                   JOIN Student ON (Transcript.StudentID = Student.ID)
                                WHERE student.StudentID = %s
                                ORDER BY Course_Catalog.name""", [studentID])
        updatedTranscriptRows = cur.fetchall()
        return render_template("Transcripts.html", things=updatedTranscriptRows)
    else:
        return render_template("TranscriptAddRemove.html")


@app.route("/transcript", methods=["POST", "GET"])
def Transcript():
    if not g.user:
        return redirect(url_for('login'))
    cur.execute("""SELECT Student.StudentID, Student.firstName, Student.lastName, Course_info.SLN, Course_Catalog.name, Course_Info.Section, Transcript.FinalGrade
                    FROM Transcript
                        JOIN Course_Info ON (Transcript.ClassID = Course_Info.ID)
                        JOIN Course_Catalog ON (Course_Info.courseid = Course_Catalog.id)
                        JOIN Student ON (Transcript.StudentID = Student.ID)
                  ORDER BY Student.StudentID""")
    updatedTranscriptRows = cur.fetchall()
    return render_template("Transcripts.html", things=updatedTranscriptRows)


def genderChecker(str):
    if str.upper() != 'F' or str.upper() != 'M':
        flash("Unacceptable Gender", "info")
        return render_template("addRemoveStudent.html")


@app.route("/add-remove-student", methods=["POST", "GET"])
def addRemoveStudent():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "POST":
        if 'add' in request.form:
            studID = request.form["studentID"]
            # StudChecker(StuID)
            cur.execute("SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s", [studID])
            exists = cur.fetchall()
            if exists.__len__() != 0:
                flash("Student already exists")
                return render_template("addRemoveStudent.html")

            Fname = request.form["first"]

            Lname = request.form["last"]

            gender = request.form["gender"]
            genderChecker(gender)

            super = request.form["super"]

            alias = request.form["alias"]

            dob = request.form["dob"]

            cur.execute('INSERT INTO Student (StudentID, FirstName, LastName, Alias, \
                Gender, SuperPower, DOB, IsCurrentlyEnrolled,adminID) \
                Values(%s,%s,%s,%s,%s,%s,%s,TRUE,1)', (int(studID), Fname, Lname, alias, gender, super, dob))
            con.commit()

            return redirect(url_for("viewStudent"))
        elif 'remove' in request.form:

            studID = int(request.form["studID"])
            cur.execute("SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s", [studID])
            exists = cur.fetchall()
            if exists.__len__() == 0:
                flash("Student doesn't exists")
                return render_template("addRemoveStudent.html")

            cur.execute("SELECT ID FROM STUDENT WHERE STUDENTID = %s", [studID])
            studID = cur.fetchall()

            cur.execute('DELETE FROM Transcript WHERE Transcript.StudentID = %s', (studID))

            # Find the noteID based on studentID, use that to delete notes
            cur.execute('SELECT NOTEID FROM Student_Notes WHERE Student_Notes.StudentID = %s', (studID))
            noteNumb = cur.fetchall()
            if noteNumb.__len__() != 0:
                cur.execute('DELETE FROM Note WHERE ID = %s', [noteNumb])

            cur.execute('DELETE FROM Student_Notes WHERE Student_Notes.StudentID = %s', (studID))
            cur.execute('DELETE FROM STUDENT WHERE ID = %s', (studID))
            con.commit()
            return redirect(url_for("viewStudent"))
        else:
            studID = request.form["studentID"]

            cur.execute("SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s", [studID])
            exists = cur.fetchall()
            if exists.__len__() == 0:
                flash("Student doesn't exists")
                return render_template("addRemoveStudent.html")

            cur.execute("SELECT ID FROM STUDENT WHERE STUDENTID = %s", [studID])
            StuID = cur.fetchall()
            StuID = StuID[0][0]

            Fname = request.form["first"]
            Lname = request.form["last"]
            gender = request.form["gender"]
            if gender.__len__() > 0:
                genderChecker(gender)

            super = request.form["super"]

            alias = request.form["alias"]

            dob = request.form["dob"]

            enr = request.form["enrollment"]
            if enr.__len__() > 0:
                if enr.upper() != "T" or enr.upper() != "F":
                    flash("Enrolled Must be T or F")
                    return render_template("addRemoveStudent.html")

            cur.execute("SELECT * FROM STUDENT WHERE ID = %s", [StuID])
            getStudentQuery = cur.fetchall()

            if Fname == "":
                qFirst = getStudentQuery[0][2]
            else:
                qFirst = Fname
            if Lname == "":
                qLast = getStudentQuery[0][3]
            else:
                qLast = Lname
            if alias == "":
                qAlias = getStudentQuery[0][4]
            else:
                qAlias = alias
            if gender == "":
                qGender = getStudentQuery[0][5]
            else:
                qGender = gender
            if super == "":
                qSuper = getStudentQuery[0][6]
            else:
                qSuper = super
            if dob == "":
                qDOB = getStudentQuery[0][7]
            else:
                qDOB = dob

            if enr == "":
                qENR = getStudentQuery[0][8]
            else:
                qENR = enr

            cur.execute('Update Student \
                SET FirstName= %s, LastName= %s, Alias= %s, \
                Gender= %s, SuperPower= %s, DOB= %s, \
                IsCurrentlyEnrolled= %s WHERE ID = %s',
                        (qFirst, qLast, qAlias, qGender, qSuper, qDOB, qENR, int(StuID)))
            con.commit()
            return redirect(url_for("viewStudent"))
    else:
        return render_template("addRemoveStudent.html")

@app.route("/course-catalog", methods=["POST", "GET"])
def courses_catalog():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("CourseCatalog.html", things=showCourseCatalogRows())


@app.route("/class-info")
def course_info():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("CourseInfo.html", things=showCourseInfoRows())


@app.route("/update-course", methods=["POST", "GET"])
def update_course():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "POST":
        oldName = request.form["oldnm"]
        name = request.form["nm"]
        credits = request.form["creds"]
        type = request.form["type"]

        # error flags
        existsInCatalog = 0  # false
        typeExists = 0  # false

        # checks for class existence in course
        if oldName != "":
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            for r in courseRows:
                curName = r[1]
                if curName == oldName:
                    existsInCatalog = 1
                    break

        # Case: If target course name doesn't exit
        if existsInCatalog == 0:
            flash("The target course doesn't exist.")
            return render_template("UpdateCourse.html")

        # checks if new class name is a duplicate
        if name != "":
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            for r in courseRows:
                curName = r[1]
                if curName == name:
                    flash("A course with that name already exists.")
                    return render_template("UpdateCourse.html")

        if type != "":
            cur.execute('Select * from Class_Type')
            typeRows = cur.fetchall()
            for r in typeRows:
                curType = r[0]
                if curType == type:
                    typeExists = 1

        # Case: if type doesn't exist
        if type == 0:
            flash("Course type doesn't exist.")
            return render_template("UpdateCourse.html")

        # Case: if nothing entered
        if (name == "" and credits == "" and type == ""):
            flash("At least one attribute must be changed.")
            return render_template("UpdateCourse.html")

        if credits != "":
            cur.execute('UPDATE Course_Catalog SET CourseCredits = %s WHERE name = %s', (credits, name))

        if type != "":
            cur.execute('UPDATE Course_Catalog SET Type = %s WHERE name = %s', (type, name))

        if name != "":
            cur.execute('UPDATE Course_Catalog SET Name = %s WHERE Name = %s', (name, oldName))

        con.commit()
        return render_template("CourseCatalog.html", things=showCourseCatalogRows())
    else:
        return render_template("UpdateCourse.html")


@app.route("/update-class", methods=["POST", "GET"])
def update_class():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "POST":
        sln = request.form["sln"]
        name = request.form["name"]
        section = request.form["section"]
        roomid = request.form["roomID"]
        instructor = request.form["instructorName"]
        time = request.form["time"]
        quarter = request.form["quarter"]
        year = request.form["year"]

        # error flags
        slnExists = 0  # false
        existsInCatalog = 0  # false
        roomExists = 0  # false
        roomHasSpace = 0  # false

        # checks if sln exits
        cur.execute('SELECT * FROM Course_Info')
        tempRows = cur.fetchall()
        for x in tempRows:
            currSln = x[2]
            if currSln == int(sln):
                slnExists = 1
                break

        # checks for room time availability
        if roomid != "":
            if time == "":
                cur.execute('SELECT * FROM Course_Info WHERE sln = %s', [sln])
                tempTime = cur.fetchall()
                time = tempTime[0][6].strftime("%H:%M:%S")
            cur.execute('SELECT * FROM Course_Info WHERE RoomID = %s', [roomid])
            tempRows = cur.fetchall()
            for x in tempRows:
                curTime = x[6]
                tempCurTime = curTime.strftime("%H:%M:%S")
                if tempCurTime == time:
                    flash("Time conflict within that building.")
                    return render_template("UpdateClass.html")

        # checks for room space and existence
        if roomid != "":
            cur.execute('SELECT * FROM Classroom')
            tempRows = cur.fetchall()
            for x in tempRows:
                curRoom = x[2]
                curCapacity = x[3]
                if (int(curRoom) == int(roomid)):
                    roomExists = 1  # true
                if (int(curCapacity) >= int(curCapacity + 1)):
                    roomHasSpace = 1  # true

        # checks for class existence in course
        if name != "":
            cur.execute('SELECT * FROM Course_Catalog')
            tempRows = cur.fetchall()
            for x in tempRows:
                curName = x[1]
                if (curName == name):
                    existsInCatalog = 1  # true
                    break

        # checks for duplicate class
        if name != "" and section != "":
            cur.execute('Select * from Course_Catalog JOIN Course_Info ON (Course_Catalog.ID = Course_Info.CourseID)')
            courseRows = cur.fetchall()
            for r in courseRows:
                curName = r[1]
                curSection = r[7]
                if (curName == name and curSection == section):
                    flash("You cannot add a class that already exists.")
                    return render_template("UpdateClass.html")

        if slnExists == 0 and sln != "":
            flash("You can't update a class that doesn't exist.")
            return render_template("UpdateClass.html")

        # Case: class not in catalog
        if existsInCatalog == 0 and name != "":
            flash("You cannot add a class to a course that doesn't exist.")
            return render_template("UpdateClass.html")

        # Case: room doesn't exist
        if roomExists == 0 and roomid != "":
            flash("You cannot add a class to a room that doesn't exist.")
            return render_template("UpdateClass.html")

        # Case: room is full
        if roomHasSpace == 0 and roomid != "":
            flash("You cannot add a class to a full room.")
            return render_template("UpdateClass.html")

        # Case: if nothing entered
        if (name == "" and section == "" and roomid == "" and instructor == ""
                and time == "" and quarter == "" and year == ""):
            flash("At least one attribute must be changed.")
            return render_template("UpdateClass.html")

        if name != "":
            cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [name])
            tempCourseID = cur.fetchall()
            newCourseID = tempCourseID[0][0]
            cur.execute('UPDATE Course_Info SET CourseID = %s WHERE sln = %s', (newCourseID, sln))

        if section != "":
            cur.execute('UPDATE Course_Info SET Section = %s WHERE sln = %s', (section, sln))

        if roomid != "":
            cur.execute('UPDATE Course_Info SET RoomID = %s WHERE sln = %s', (roomid, sln))

        if instructor != "":
            cur.execute('UPDATE Course_Info SET InstructorName = %s WHERE sln = %s', (instructor, sln))

        if time != "":
            cur.execute('UPDATE Course_Info SET Time = %s WHERE sln = %s', (time, sln))

        if quarter != "":
            cur.execute('UPDATE Course_Info SET Quarter = %s WHERE sln = %s', (quarter, sln))

        if year != "":
            cur.execute('UPDATE Course_Info SET Year = %s WHERE sln = %s', (year, sln))

        con.commit()
        return render_template("CourseInfo.html", things=showCourseInfoRows())
    else:
        return render_template("UpdateClass.html")


@app.route("/add-course", methods=["POST", "GET"])
def add():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "POST":

        # check if its an add or remove
        if 'add' in request.form:
            # request data
            name = request.form["nm"]
            cc = request.form["creds"]
            type = request.form["type"]

            if (name and cc and type):
                # checks if course already exists
                cur.execute('Select * from Course_Catalog')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]

                    if (curName == name):
                        flash("You cannot add a course that already exists.", "error")
                        return render_template("AddCourse.html")

                # adds to course catalog
                cur.execute("""INSERT INTO Course_Catalog (Name, CourseCredits, Type) 
                                VALUES (%s, %s, %s)""", (name, cc, type))

                # update table
                cur.execute('Select * from Course_Catalog')
                courseRows = cur.fetchall()
                con.commit()

                return render_template("CourseCatalog.html", things=showCourseCatalogRows())
            else:
                flash("Fill in necessary information.")
                return render_template("AddCourse.html")
        else:
            name = request.form["nm"]
            if (name):
                # checks if course doesn't exist
                cur.execute('Select * from Course_Catalog')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]

                    if (curName == name):
                        courseExist = 1  # true
                        # removes course from course catalog
                        cur.execute("""DELETE FROM Course_Catalog WHERE Name = %s""", [name])
                        con.commit()

                        return render_template("CourseCatalog.html", things=showCourseCatalogRows())
                    else:
                        courseExist = 0  # false

                if (courseExist == 0):
                    flash("You cannot remove a course that doesn't exists.", "error")
                    return render_template("AddCourse.html")
            else:
                flash("Fill in necessary information.")
                return render_template("AddCourse.html")
    else:
        return render_template("AddCourse.html")


@app.route("/add-class", methods=["POST", "GET"])
def addClass():
    if not g.user:
        return redirect(url_for('login'))
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

            if (name and section and roomid and instructor and time and quarter and year):
                # error flags
                existsInCatalog = 0  # false
                roomExists = 0  # false
                roomHasSpace = 1  # false
                roomAvailable = 1  # true

                # checks for room time availability
                cur.execute('SELECT * FROM Course_Info WHERE RoomID = %s', [roomid])
                tempRows = cur.fetchall()
                for x in tempRows:
                    curTime = x[6]
                    tempCurTime = curTime.strftime("%H:%M:%S")
                    tempTime = time + ':00'
                    if (tempCurTime == tempTime):
                        roomAvailable = 0  # false

                # checks for room space and existence 
                cur.execute('SELECT * FROM Classroom')
                tempRows = cur.fetchall()
                for x in tempRows:
                    curRoom = x[2]

                    curCapacity = x[3]
                    if (int(curRoom) == int(roomid)):
                        roomExists = 1  # true
                    if (int(curCapacity) >= int(curCapacity + 1)):
                        roomHasSpace = 1  # true

                # checks for class existence in course
                cur.execute('SELECT * FROM Course_Catalog')
                tempRows = cur.fetchall()
                for x in tempRows:
                    curName = x[1]
                    if (curName == name):
                        existsInCatalog = 1  # true

                # checks for duplicate class
                cur.execute(
                    'Select * from Course_Catalog JOIN Course_Info ON (Course_Catalog.ID = Course_Info.CourseID)')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]
                    curSection = r[7]

                    if (curName == name and curSection == section):
                        flash("You cannot add a class that already exists.")
                        return render_template("AddClass.html")

                # Case: class time conflict
                if roomAvailable == 0:
                    flash("Time conflict within that building.")
                    return render_template("AddClass.html")

                # Case: class not in catalog
                if existsInCatalog == 0:
                    flash("You cannot add a class to a course that doesn't exist.")
                    return render_template("AddClass.html")

                # Case: room doesn't exist
                if roomExists == 0:
                    flash("You cannot add a class to a room that doesn't exist.")
                    return render_template("AddClass.html")

                # Case: room is full
                if roomHasSpace == 0:
                    flash("You cannot add a class to a full room.")
                    return render_template("AddClass.html")

                # adds to course info
                cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [name])
                idEntry = cur.fetchall()
                id = idEntry[0][0]

                cur.execute("""INSERT INTO Course_Info (CourseID, Section, RoomID, InstructorName, Time, Quarter, Year) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (id, section, roomid, instructor, time, quarter, year))

                con.commit()

                # update table
                cur.execute('Select * from Course_Info')
                courseInfoRows = cur.fetchall()
                con.commit()

                return render_template("courseInfo.html", things=showCourseInfoRows())
            else:
                flash("Fill in necessary information.")
                return render_template("AddClass.html")
        else:
            # request data
            name = request.form["name"]
            section = request.form["section"]

            if (name and section):
                # for class delete only name and section are needed
                # checks if class doesn't exist in course_Info 
                cur.execute(
                    'Select * from Course_Catalog JOIN Course_Info ON (Course_Catalog.ID = Course_Info.CourseID)')
                courseRows = cur.fetchall()
                for r in courseRows:
                    curName = r[1]
                    curSection = r[7]

                    if (curName == name and curSection == section):
                        courseExist = 1  # true
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
                        courseExist = 0  # false

                if (courseExist == 0):
                    flash("You cannot remove a class that doesn't exists.", "error")
                    return render_template("AddClass.html")
            else:
                flash("Fill in necessary information.")
                return render_template("AddClass.html")
    else:
        # show main screen initially
        return render_template("AddClass.html")


@app.route("/view-student-notes", methods=["POST", "GET"])
def viewStudentNotes():
    if not g.user:
        return redirect(url_for('login'))
    studentNotes = func.viewStudentNotes()
    if request.method == "POST":

        if 'modifyNotes' in request.form:
            studentNotes = func.viewStudentNotes()
            return render_template('ModifyStudentNotes.html', things=studentNotes)

        if 'viewNotes' in request.form:
            theStudentID = request.form["theirID"]

            if (theStudentID != ""):

                if (theStudentID.isdecimal() == 0):
                    flash("StudentID must be a number", "error")
                    return render_template("ViewStudentNotes.html", things=studentNotes)

                specificStudent = func.viewSpecificStudentNotes(theStudentID)
                return render_template("ViewStudentNotes.html", things=specificStudent)
            else:
                return render_template("ViewStudentNotes.html", things=studentNotes)

    studentNotes = func.viewStudentNotes()
    return render_template("ViewStudentNotes.html", things=studentNotes)


@app.route("/modify-student-notes", methods=["POST", "GET"])
def modifyStudentNotes():
    if not g.user:
        return redirect(url_for('login'))
    studentNotes = func.viewStudentNotes()
    if request.method == "POST":
        if 'viewNotes' in request.form:
            print("clicked viewNotes")
            studentNotes = func.viewStudentNotes()
            return render_template('ViewStudentNotes.html')

        if 'delete' in request.form:
            print("DELETE WAS RANNNN")
            theStudentID = request.form["theirID"]

            theNoteID = request.form["NoteID"]

            if (theNoteID.isdecimal() == 0 or theStudentID.isdecimal() == 0):
                flash("Please enter a valid NoteID and StudentID", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)

            print("after first if")
            doesNoteExist = """ select * from Note where NoteID = %s; """

            doesStudentHaveBoth = """select * from student_notes where studentID = %s; """

            allRowsStudentNotes = """select * from student_notes """
            isStudentLinkedWithNote = """select StudentID, Student_notes.NoteID, Note.NoteID from student_notes
                                         JOIN Note ON (student_notes.noteID = Note.ID)   
                                         where studentID = %s AND Note.NoteID = %s;  """

            cur.execute(isStudentLinkedWithNote, (theStudentID, theNoteID))
            linkedwithnotequery = cur.fetchall()

            linkedstud = 0
            linkednote = 0
            for x in linkedwithnotequery:
                studid = x[0]
                noteid = x[2]
                if (str(studid) == theStudentID):
                    linkedstud = 1
                if (str(noteid) == theNoteID):
                    linkednote = 1
            if (linkedstud == 0 or linkednote == 0):
                flash("Please enter a valid NoteID and StudentID combination", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)

            cur.execute(allRowsStudentNotes)
            allRowsQuery = cur.fetchall()
            print(allRowsQuery)

            cur.execute(doesStudentHaveBoth, (theStudentID,))
            studentIDExists = 0
            NoteIDExists = 0
            tempRows = cur.fetchall()  # does studentid exist
            print(tempRows)

            for x in tempRows:
                curStudID = x[0]
                if (str(curStudID) == theStudentID):
                    studentIDExists = 1  # true
                    print("student id exists")

            cur.execute(doesNoteExist, (theNoteID,))
            noteQuery = cur.fetchall()
            print(noteQuery)
            for r in noteQuery:
                curNotID = r[1]
                if (str(curNotID) == theNoteID):
                    NoteIDExists = 1
                    print("note id exists")

            if (studentIDExists == 0 or NoteIDExists == 0):
                flash("Please enter a valid NoteID and StudentID", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)

            noteQuery = """ delete from note where note.noteID = %s """
            getSerial = """select ID from note where NoteID = %s """
            cur.execute(getSerial, (theNoteID,))
            NoteSerialNotInForm = cur.fetchall()
            noteSerialInForm = NoteSerialNotInForm[0][0]

            student_notesQuery = """ delete from Student_Notes where student_notes.StudentID = %s AND student_notes.noteID = %s; """
            cur.execute(student_notesQuery, (theStudentID, noteSerialInForm))
            con.commit()
            cur.execute(noteQuery, (theNoteID,))
            con.commit()
            studentNotes = func.viewStudentNotes()  # calls viewStudentNotes
            flash("Successfully deleted note")
            return render_template(
                "ModifyStudentNotes.html")  # passes studentNotes to page 'studentNotes.html' to have it's contents printed to screen


        elif 'add' in request.form:
            print("WENT THROUGH ADD")
            theStudentID = request.form["theirID"]
            note = request.form["notes"]
            noteType = request.form["noteType"]
            theDate = request.form["date"]
            if theStudentID == "" or note == "" or theDate == "":
                flash("Please enter a valid StudentID, note and date", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)

            splitDate = theDate.split("/")
            if len(splitDate) != 3:
                flash("Please enter a valid date", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)
            month = splitDate[0]
            day = splitDate[1]
            year = splitDate[2]

            if (month.isdecimal() == 0 or day.isdecimal() == 0 or year.isdecimal() == 0):
                flash("Please enter a valid date", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)
            month = int(splitDate[0])
            day = int(splitDate[1])
            year = int(splitDate[2])

            if (month > 12 or month < 1):
                flash("Please enter a valid date", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)
            if (day > 31 or day < 1):
                flash("Please enter a valid date", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)
            if (year > 2021 or year < 1):
                flash("Please enter a valid date", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)

            dateObject = datetime.datetime(year, month, day)
            curDate = date.today()

            if (dateObject > datetime.datetime.now()):
                flash("Please enter a date that is prior to today", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)
            print(dateObject)
            print(date.today())
            # theNoteID = request.form["NoteID"]

            if (theStudentID.isdecimal() == 0):
                flash("Please enter a valid StudentID", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)

            studentQuery = """select * from student where ID = %s; """
            cur.execute(studentQuery, (theStudentID,))

            studentQueryResult = cur.fetchall()
            print(studentQueryResult)
            studentIDExists = 0
            for x in studentQueryResult:
                curStudID = x[0]

                print(type(theStudentID))
                if (str(curStudID) == theStudentID):
                    studentIDExists = 1  # true
                    print("went throughout checks ")
            print(studentIDExists)
            if (studentIDExists == 0):
                flash("Please enter a valid StudentID", "error")
                return render_template("ModifyStudentNotes.html", things=studentNotes)
            print("went throughout checks ")

            findMaxNoteID = """Select MAX(NoteID) from Note"""  # find max note from Note
            cur.execute(findMaxNoteID)
            maxNotInForm = cur.fetchall()
            max = maxNotInForm[0][0]  # get max note because idk how we are keeping track of noteID
            max = max + 1
            adminID = 1
            currentDate = date.today()
            studentInsert = """INSERT INTO Note (NoteID, Note, Date, Type, AdminID)
                                Values(%s, %s, %s, %s, %s);"""  # OKAY so apparently I need to insert into Note first and then connect that to Student Notes
            # by creating the note and then saying "insert into student_Notes where the Student_Notes.NoteID == Note.ID (the note that I just created in the Note table"
            studentNotesInsert = """INSERT INTO Student_Notes (NoteID, StudentID) Values (%s, %s);"""

            # print(max, note, currentDate, noteType, adminID )

            cur.execute(studentInsert, (max, note, dateObject, noteType,
                                        adminID))  # here trying to insert the studentID and notID into the student_notes table
            con.commit()
            getSerial = """SELECT Note.ID from Note where Note.NoteID = %s;"""
            cur.execute(getSerial, (max,))
            theSerial = cur.fetchall()
            serialRightForm = theSerial[0][0]

            cur.execute(studentNotesInsert, (serialRightForm, theStudentID))
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
            # print(studentNotesRows)
            studentNotes = func.viewStudentNotes()
            allStudents = func.viewAllStudents()
            flash("Note successfully added", "info")
            return render_template("ModifyStudentNotes.html", things=studentNotes)
        print("post")
        studentNotes = func.viewStudentNotes()  # calls viewStudentNotes
        return render_template("ModifyStudentNotes.html", things=studentNotes)
    print("no post")
    studentNotes = func.viewStudentNotes()  # calls viewStudentNotes
    return render_template("ModifyStudentNotes.html", things=studentNotes)


if __name__ == "__main__":
    app.run(debug=True)

# close cursor
cur.close()

# close the connection
con.close()
