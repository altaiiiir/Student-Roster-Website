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

print(id) 
#execute query
cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)')
courseInfoRows = cur.fetchall()

#execute query
cur.execute('SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID) JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) JOIN Student ON (Student.ID = Transcript.StudentID) WHERE Course_Info.SLN = 10000 AND Course_Info.RoomID = 5')
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

        # request data
        name = request.form["nm"]
        cc = request.form["creds"]
        type = request.form["type"]

        # check if its an add or remove
        if 'add' in request.form:
            # adds to course catalog
            cur.execute("""INSERT INTO Course_Catalog (Name, CourseCredits, Type) 
                            VALUES (%s, %s, %s)""", (name, cc, type))

            # update table
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            con.commit()

            return render_template("courseInfoPage.html", things = courseRows)
        else:
            # removes course from course catalog
            cur.execute("""DELETE FROM Course_Catalog WHERE Name = %s""", [name])
            con.commit()

            # update table
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            
            return render_template("coursePage.html", things = courseRows)
    else:
        return render_template("addCourse.html")

@app.route("/addClass", methods = ["POST", "GET"])
def add():
    if request.method == "POST":

        # request data
        name = request.form["nm"]
        cc = request.form["creds"]
        type = request.form["type"]

        # check if its an add or remove
        if 'add' in request.form:
            # adds to course catalog
            cur.execute("""INSERT INTO Course_Catalog (Name, CourseCredits, Type) 
                            VALUES (%s, %s, %s)""", (name, cc, type))

            # update table
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            con.commit()

            return render_template("courseInfoPage.html", things = courseRows)
        else:
            # removes course from course catalog
            cur.execute("""DELETE FROM Course_Catalog WHERE Name = %s""", [name])
            con.commit()

            # update table
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            
            return render_template("coursePage.html", things = courseRows)
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