from extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(150),unique=True,nullable=False)
    password= db.Column(db.String(255),nullable=False)
    email= db.Column(db.String(255),unique=True,nullable=False)
    profile_picture= db.Column(db.String(255),nullable=True)
    date_joined = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    tracked_habits = db.relationship('TrackedHabit', backref='user',lazy=True, cascade="all, delete", passive_deletes=True)
    goals = db.relationship('Goal',backref='user',lazy=True)

    def __repr__(self):
        return f'<User: {self.username} Email: {self.email}>'
    def get_id(self):
        return self.id    

class Habit(db.Model):

    __tablename__ = 'habit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(50), nullable=False)

    tracked_habits = db.relationship('TrackedHabit', backref='habit',lazy=True)

class HabitLog(db.Model):
    __tablename__ = 'habitlog'

    id = db.Column(db.Integer, primary_key=True)
    tracked_habit_id = db.Column(db.Integer, db.ForeignKey('tracked_habit.id'), nullable=False)
    date_logged = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed = db.Column(db.Boolean, default=False)

class TrackedHabit(db.Model):
    __tablename__ = 'tracked_habit'
    #__table_args__ = {'schema': 'new_schema'} 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    habit_name = db.Column(db.String(100), nullable=False)
    habit_id = db.Column(db.Integer,db.ForeignKey('habit.id'),nullable=False)
    streak = db.Column(db.Integer,default=0)
    last_completed = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    logs = db.relationship('HabitLog', backref='tracked_habit', lazy=True)
    goal = db.relationship('Goal', backref='tracked_habit', uselist=False, cascade='all, delete-orphan',passive_deletes=True) #one-to-one relationship

class Milestone(db.Model):
    __tablename__ = 'milestone'

    id = db.Column(db.Integer, primary_key=True)
    streak_days = db.Column(db.Integer,nullable=False)
    #achieved_on = db.Column(db.DateTime(timezone=True),default=lambda: datetime.now(timezone.utc)) dropped for now

class Goal(db.Model):
    __tablename__ = 'goal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    tracked_habit_id = db.Column(db.Integer,db.ForeignKey('tracked_habit.id', ondelete='CASCADE'),nullable=False)
    goal_freq = db.Column(db.Integer, default=1)
    goal_type = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

