from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bigballz4()$loveUUUIII@localhost/test'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] =''


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#class Feedback(db.Model):


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        #print (customer, dealer, rating, comments)

        if customer == '' or dealer == '':
            return render_template('index.html', message = 'enter required fields')

        return render_template('success.html')

if __name__ == '__main__':
    app.debug = True
    app.run()