from flask import Flask, request, render_template
from flask import redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)


class User(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(20), unique=True, nullable=False)
	email=db.Column(db.String(120),unique=True, nullable=False)
	image_file=db.Column(db.String(120),nullable=False, default='default.jpg')
	password=db.Column(db.String(120),nullable=False)
	tasks=db.relationship('todo',backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username},{self.email},{self.image_file}')"


class todo(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	task=db.Column(db.Text,nullable=False)
	date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	done = db.Column(db.Boolean, default=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __init__(self, task):
		self.task=task
		self.done=False
        
	def __repr__(self):
		return f"todo('{self.task},{self.date}')"
db.drop_all()
db.create_all()





@app.route('/')
def task_list():
	tasklist= todo.query.all()
	return render_template('test.html',tasklist=tasklist)
@app.route('/task')
def add_task():
	task=request.form('task')
	tasklist=todo(task)
	db.session.add(tasklist)
	db.session.commit()







