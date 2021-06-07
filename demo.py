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
    if str.upper() != 'F' or str.upper() != 'M':
        flash("Unacceptable Gender","info")
        return render_template("addRemoveStudent.html")


@app.route("/") 
def home():
    cur.execute('Select * from Student')
    rows = cur.fetchall()
    return render_template("studentPage.html", things=rows)



@app.route("/addRemoveStudent", methods = ["POST","GET"]) 
def addRemoveStudent():
    if request.method == "POST":
        if 'add' in request.form:
            StuID = request.form["studentID"]
            # StudChecker(StuID)
            cur.execute("SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s",[StuID])
            exists= cur.fetchall()
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
                Values(%s,%s,%s,%s,%s,%s,%s,TRUE,1)',(int(StuID),Fname,Lname,alias,gender,super,dob))
            con.commit()
            return redirect(url_for("home"))
        elif 'remove' in request.form:
            
            studID = int(request.form["studID"])
            cur.execute("SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s",[studID])
            exists= cur.fetchall()
            if exists.__len__() == 0:
                flash("Student doesn't exists")
                return render_template("addRemoveStudent.html")
          
            cur.execute("SELECT ID FROM STUDENT WHERE STUDENTID = %s",[studID])
            studID = cur.fetchall()
            
            cur.execute('DELETE FROM Transcript WHERE Transcript.StudentID = %s',(studID))
           
            # Find the noteID based on studentID, use that to delete notes
            cur.execute('SELECT NOTEID FROM Student_Notes WHERE Student_Notes.StudentID = %s',(studID))
            noteNumb = cur.fetchall()
            if noteNumb.__len__() != 0:
                cur.execute('DELETE FROM Note WHERE ID = %s',[noteNumb])

            cur.execute('DELETE FROM Student_Notes WHERE Student_Notes.StudentID = %s',(studID))
           
    
            cur.execute('DELETE FROM STUDENT WHERE ID = %s',(studID))
            return redirect(url_for("home"))
        else:
            StuID = request.form["studentID"]
            
            cur.execute("SELECT STUDENTID FROM STUDENT WHERE STUDENTID = %s",[StuID])
            exists= cur.fetchall()
            if exists.__len__() == 0:
                flash("Student doesn't exists")
                return render_template("addRemoveStudent.html")

            cur.execute("SELECT ID FROM STUDENT WHERE STUDENTID = %s",[StuID])
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
        
            cur.execute("SELECT * FROM STUDENT WHERE ID = %s",[StuID])
            getStudentQuery = cur.fetchall()
            print(getStudentQuery)
            #[(19, 24, 'first', 'last', 'gff', 'M', 'gayaf', datetime.date(2005, 4, 8), True, 1)]
            if Fname == "":
                qFirst = getStudentQuery[0][2]
            else:
                qFirst = Fname
            
            if Lname == "":
                qLast = getStudentQuery[0][3]
            else:
                qLast = Fname
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
                IsCurrentlyEnrolled= %s WHERE ID = %s' ,(qFirst,qLast,qAlias,qGender,qSuper,qDOB,qENR,int(StuID)))
            con.commit()
            return redirect(url_for("home"))               
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
