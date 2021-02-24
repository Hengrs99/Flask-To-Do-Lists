from . import db
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    lists = db.relationship('List')

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    finished = db.Column(db.Boolean)
    tasks = db.relationship('Task')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    finished = db.Column(db.Boolean)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
