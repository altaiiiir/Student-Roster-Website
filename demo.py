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


# close cursor
cur.close()

#close the connection
con.close()

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


@app.route("/courses") 
def course():
    return render_template("coursePage.html", things = courseRows)

    
if __name__ == "__main__":
     app.run(debug =True)