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

#execute query
cur.execute('Select * from Student')
rows = cur.fetchall()

for r in rows:
   print(f"ID {r[0]} name {r[1]}")

#execute query
cur.execute('Select * from Course_Catalog')
courseRows = cur.fetchall()

for r in courseRows:
   print(f"SLN {r[0]} Name {r[1]} CourseCredits {r[2]} Type {r[3]}")

#execute query
cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)')
courseInfoRows = cur.fetchall()

#execute query
cur.execute('SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN) JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) JOIN Student ON (Student.ID = Transcript.StudentID) WHERE Course_Info.SLN = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

# close cursor
#cur.close()

#close the connection
#con.close()

app = Flask(__name__)

@app.route("/") 
def home():
    return render_template("studentPage.html", things = rows)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr = user))
    else:
        return render_template("login.html")




@app.route("/courseInfo") 
def courseInfo():
    return render_template("courseInfoPage.html", things = courseInfoRows)

@app.route("/courseAttendees") 
def courseAttendees():
    return render_template("courseAttendees.html", things = courseAttendeesRows)

@app.route("/addCourse", methods = ["POST", "GET"])
def add():
    if request.method == "POST":
        sln = request.form["sln"]
        section = request.form["section"]
        roomid = request.form["roomid"]
        instructor = request.form["ins"]
        time = request.form["time"]
        quarter = request.form["quarter"]
        year = request.form["yr"]
        name = request.form["nm"]
        cc = request.form["creds"]
        type = request.form["type"]
        cur.execute("""INSERT INTO Course_Catalog (SLN, Name, CourseCredits, Type) 
                        VALUES (%s, %s, %s, %s)""", (sln, name, cc, type))
        cur.execute("""INSERT INTO Course_Info (SLN, Section, RoomID, InstructorName, Time, Quarter, Year) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""", (sln, section, roomid, instructor, time, quarter, year))
        con.commit()
        # update table
        cur.execute('Select * from Course_Catalog')
        courseRows = cur.fetchall()
        
        # update table
        cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.SLN = Course_Catalog.SLN)')
        courseInfoRows = cur.fetchall()
        
        return render_template("courseInfoPage.html", things = courseInfoRows)
    else:
        return render_template("addCourse.html")

@app.route("/courses") 
def course():
    return render_template("coursePage.html", things = courseRows)


if __name__ == "__main__":
     app.run(debug =True)
     
     
     
# close cursor
cur.close()

#close the connection
con.close()