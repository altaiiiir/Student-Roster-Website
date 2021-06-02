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

#execute query
cur.execute('Select * from Student')
rows = cur.fetchall()

for r in rows:
   print(f"ID {r[0]} name {r[1]}")

#execute courses query
cur.execute('Select * from Course_Catalog')
courseRows = cur.fetchall()



app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/") 
def home():
    return render_template("index.html", things=rows)

@app.route("/studentPage", methods=["POST", "GET"]) 
def studentPage():
    if request.method == "POST":
        session.permanant = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("studentPage.html", things=rows)
    
# @app.route("/test")
# def test():
#     return render_template("new.html")

@app.route("/courseCatalog", methods=["POST", "GET"])
def courseCatalog():
    if request.method == "POST":
        creditType = request.form["courseType"]
        SLN = request.form["SLN"]
        cur.execute('Select * from Course_Catalog WHERE Type = %s AND SLN = %d', (creditType, SLN))
        creditRows = cur.fetchall()
        for r in creditRows:
            print(f"ID {r[0]} name {r[1]}")
        return render_template("courseCatalog.html", things=creditRows)
    else:
        return render_template("courseCatalog.html", things=courseRows) 

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user} </h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("studentPage"))

if __name__ == "__main__":
     app.run(debug =True)

# close cursor
cur.close()

#close the connection
con.close()