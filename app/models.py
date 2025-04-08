from extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone


class User(db.Model, UserMixin):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(150),unique=True,nullable=False)
    password= db.Column(db.String(255),nullable=False)
    email= db.Column(db.String(255),unique=True,nullable=False)
    profile_picture= db.Column(db.String(255),nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User: {self.username} Email: {self.email}>'
    def get_id(self):
        return self.id    

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date_logged = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    completed = db.Column(db.Boolean, default=False)

class TrackedHabit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    habit_id = db.Column(db.Integer,db.ForeignKey('habit.id'),nullable=False)
    date_logged = db.Column(db.DateTime)
    date_logged = db.Column(db.DateTime)
    streak = db.Column(db.Integer,default=0)
    last_completed = db.Column(db.DateTime)

class Milestones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    habit_name = db.Column(db.String(255), nullable=False)
    criteria = db.Column(db.String(125),nullable=False)

class Goal(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    habit_id = db.Column(db.Integer,db.ForeignKey('habit.id'),nullable=False)
    goal_type = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))