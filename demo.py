import psycopg2, datetime
from re import split
from flask import Flask, redirect, url_for, render_template, request, session, flash, g

from datetime import timedelta, datetime
import datetime
from datetime import date



#connect to the local host db
con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

#cursor
cur = con.cursor()

app = Flask(__name__)
# app = Flask(name)
app.secret_key = 'asrtarstaursdlarsn'

def StringChecker(str,name):
    for x in str:
        if (ord(x) >= 65 or ord(x) <= 95) and \
            (ord(x) >= 97 or ord(x) <= 122):
             continue
        else:
            flash(name + " should contain letters only","info")
            return render_template("addRemoveStudent.html")

def genderChecker(str):
    if str.isspace() or str == "":
        flash("Cannot be empty")
        return render_template("addRemoveStudent.html")
    elif str.upper() != 'F' or str.upper() != 'M':
        flash("Unacceptable Gender","info")
        return render_template("addRemoveStudent.html")

def dobChecker(str):
    try: 
        dateObject = datetime.strptime(str,'%d/%m/%y')
        DOB = str.split("/")
    except:
        flash("Invalid DOB")
        return render_template("addRemoveStudent.html")

def StudChecker(str):
    cur.execute("SELECT EXISTS (SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s)",[str])
    exists= cur.fetchall()
    if exists:
        flash("Student already exists")
        return render_template("addRemoveStudent.html")

def notStudChecker(str):
    cur.execute("SELECT EXISTS (SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s)",[str])
    exists= cur.fetchall()
    if not exists:
        flash("Student doesn't exist")
        return render_template("addRemoveStudent.html")

@app.route("/") 
def home():
    cur.execute('Select * from Student')
    rows = cur.fetchall()
    return render_template("studentPage.html", things=rows)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr =user))
    else:
        return render_template("login.html")



@app.route("/addRemoveStudent", methods = ["POST","GET"]) 
def addRemoveStudent():
    if request.method == "POST":
        if 'add' in request.form:
            StuID = request.form["studentID"]
            StudChecker(StuID)

            Fname = request.form["first"]
            StringChecker(Fname,"First name")
            
            Lname = request.form["last"]
            StringChecker(Lname,"Last name")
           
            gender = request.form["gender"]
            genderChecker(gender)
            
            super = request.form["super"]
            StringChecker(super,"Super abilities")
            
            alias = request.form["alias"]
            StringChecker(alias,"Alias")
            
            dob = request.form["dob"]
            dobChecker(dob)

            cur.execute('INSERT INTO Student (StudentID, FirstName, LastName, Alias, \
                Gender, SuperPower, DOB, IsCurrentlyEnrolled,adminID) \
                Values(%s,%s,%s,%s,%s,%s,%s,TRUE,1)',(int(StuID),Fname,Lname,alias,gender,super,dob))
            con.commit()
            return redirect(url_for("home"))
        elif 'remove' in request.form:

            studID = int(request.form["studID"])
            notStudChecker(studID)
          
            cur.execute("SELECT ID FROM STUDENT WHERE STUDENTID = %s",[studID])
            studID = cur.fetchall()
            
            cur.execute('DELETE FROM Transcript WHERE Transcript.StudentID = %s',[studID])
           
            # Find the noteID based on studentID, use that to delete notes
            cur.execute('SELECT NOTEID FROM Student_Notes WHERE Student_Notes.StudentID = %s',[studID])
            noteNumb = cur.fetchall()
            cur.execute('DELETE FROM Note WHERE ID = %s',[noteNumb])
            
            cur.execute('DELETE FROM Student_Notes WHERE Student_Notes.StudentID = %s',[studID])
            cur.execute('DELETE FROM STUDENT WHERE ID = %s',[studID])
            return redirect(url_for("home"))
        else:
            StuID = request.form["studentID"]
            notStudChecker(StuID)

            Fname = request.form["first"]
            StringChecker(Fname,"First name")

            Lname = request.form["last"]
            StringChecker(Lname,"Last name")

            gender = request.form["gender"]
            genderChecker(gender)
            
            super = request.form["super"]
            StringChecker(super,"Super abilities")
            
            alias = request.form["alias"]
            StringChecker(alias,"Alias")
            
            dob = request.form["dob"]
            dobChecker(dob)

            enr = request.form["enrollment"]
            if enr.upper() != "T" or enr.upper() != "F":
                flash("Must be T or F")
                return render_template("addRemoveStudent.html")
            if (StuID == ""):
                flash("Enter studentID", "error")
                return render_template("addRemoveStudent.html")

            studentQuery = """select * from Student where student.ID = %s """ 
            cur.execute(studentQuery, (StuID,))
            getStudentQuery = cur.fetchall()

            if Fname == "":
                qFirst = getStudentQuery[0][0]
            else:
                qFirst = Fname
            
            if Lname == "":
                qLast = getStudentQuery[0][1]
            else:
                qLast = Fname
            if gender == "":
                qGender = getStudentQuery[0][2] 
            else:
                qGender = gender
            if super == "":
                qSuper = getStudentQuery[0][3]
            else:
                qSuper = super
            if alias == "":
                qAlias = getStudentQuery[0][4]
            else:
                qAlias = alias
            if dob == "":
                qDOB = getStudentQuery[0][5]
            else:
                qDOB = dob
            if enr == "":
                qENR = getStudentQuery[0][6]
            else:
                qENR = enr


            cur.execute('Update Student \
                SET FirstName= %s, LastName= %s, Alias= %s, \
                Gender= %s, SuperPower= %s, DOB= %s, \
                IsCurrentlyEnrolled= %s WHERE StudentID = %s' ,(qFirst,qLast,qAlias,qGender,qSuper,qDOB,qENR,int(StuID)))
            con.commit()
            return redirect(url_for("home"))
        return render_template("addRemoveStudent.html")
            # cur.execute('Update Student \
            # SET FirstName= %s, LastName= %s, Alias= %s, \
            # Gender= %s, SuperPower= %s, DOB= %s, \
            # IsCurrentlyEnrolled= %s WHERE StudentID = %s' ,(Fname,Lname,alias,gender,super,dob,enr,int(StuID)))
            #con.commit()
               
    else:
        return render_template("addRemoveStudent.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr} </h1>"

if __name__ == "__main__":
    app.run(debug =True)


# close cursor
cur.close()

#close the connection
con.close()
