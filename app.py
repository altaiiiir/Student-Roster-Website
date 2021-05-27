from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route("/home")
def home():
    return "<h1> HELLO <h1>"



@app.route("/view", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            print ("view all students")
        elif request.form['submit_button'] == 'Do Something Else':
            print ("view specific student")
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run()