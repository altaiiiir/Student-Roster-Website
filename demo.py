import psycopg2
from flask import Flask, redirect, url_for, render_template, request

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
            #need to double check data, protect against sql injections
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
            return redirect(url_for("home"))
        else:
            #need to double check data, protect against sql injections
            studID = int(request.form["studID"])
            # studID = request.form["studID"]
            cur.execute('DELETE FROM Transcript WHERE Transcript.StudentID = %s',[studID])
            cur.execute('DELETE FROM Student_Notes WHERE Student_Notes.StudentID = %s',[studID])
            cur.execute('DELETE FROM STUDENT WHERE ID = %s',[studID])
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
