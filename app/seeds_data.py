from extensions import db
from models import Habit, Goal, Milestone

#separate file for pre defined data
def seed_habits():

    habits = [
        {"name":"Read","description": "Read a few pages or chapter of a book","category": "Mind"},
        {"name":"Exercise","description": "Hit the gym and burn some calories","category": "Fitness"},
        {"name":"Study","description": "Have a focused study session","category": "Mind"},
        {"name":"Meditate","description": "Some quiet time","category": "Mind"},
        {"name":"Jogging","description": "Jog your system with some running","category": "Fitness"},
        {"name":"Custom","description":"Any of your choosing","category":"Custom"}
    ]

    for habit in habits: #add habits to db if not already added
        exists = Habit.query.filter_by(name = habit['name']).first()
        if not exists:
            db.session.add(Habit(**habit)) #unpack dictionary item and add new habit to db
            db.session.commit()

default_milestones = [3,7,14,30,50,100,200,250,300,365]
def seed_milestones():
    for streak_days in default_milestones:
        milestone = Milestone.query.filter_by(streak_days=streak_days).first()
        if not milestone:
            db.session.add(Milestone(streak_days=streak_days))
            db.session.commit()

def run_all_seeds():
    seed_habits()
    seed_milestones()