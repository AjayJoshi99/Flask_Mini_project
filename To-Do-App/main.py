#.\env\Scripts\activate.ps1  --> to activate virtual environment

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/')
def hello_World():
    return render_template('home.html')


@app.route('/hello', methods=['GET', 'POST'])  #http://127.0.0.1:5000/hello
def hello():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()
        # print(request.form['title'])
        # print('Post')
    allToDo = ToDo.query.all()
    return render_template('index.html', allToDo=allToDo)


@app.route('/show')
def display():
    allToDo = ToDo.query.all()
    print(allToDo)  # prints in console
    return "Hello"


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/hello')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/hello')
    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    app.run(debug=True)

'''
--> write below code in python for creating todo.db
from main import db, app

with app.app_context():
    db.create_all()
'''

