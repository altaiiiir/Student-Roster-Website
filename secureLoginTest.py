from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import psycopg2
import func


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='password'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route('/', methods=['GET', 'POST'])
def secureLogin():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('secureLogin'))

    return render_template('secureLogin.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('secureLogin'))

    return render_template('profile.html')


@app.route("/home") 
def home():
    if not g.user:
        return redirect(url_for('secureLogin'))
    return render_template("home.html")

if __name__ == "__main__":
     app.run(debug =True)