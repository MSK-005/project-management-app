from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String)
    description = db.Column(db.String)
    priority = db.Column(db.String)
    date_of_creation = db.Column(db.DateTime(timezone=True), default=func.now())
    due_date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    tasks = db.relationship('Task')