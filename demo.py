from func import viewCourseCatalog
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

transRows = cur.fetchall()
# close cursor
cur.close()

#close the connection
con.close()

app = Flask(__name__)

@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/studentPage", methods =['GET', 'POST'])
def students():
    return render_template("studentPage.html", things = rows)

@app.route("/courseCatalog")
def courseCatalog():
    courseCatalog = viewCourseCatalog()
    return render_template("courseCatalog.html", things=courseCatalog)


#@app.route("/login", methods=["POST", "GET"])
#def login():
 #   if request.method == "POST":
  #      user = request.form["nm"]
   #     return redirect(url_for("user", usr =user))
    ##   return render_template("login.html")

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
    
if __name__ == "__main__":
     app.run(debug =True)