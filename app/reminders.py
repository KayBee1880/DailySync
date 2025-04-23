# reminders.py
from flask import current_app
from models import User, HabitLog 
from extensions import db, mail  
from flask_mail import Message
from support import get_weekly_logs

def generate_habits_to_remind(user):
    habits_to_remind = []
    current_week, _ = get_weekly_logs()
    for habit in user.tracked_habits:
        logs_this_week = HabitLog.query.filter(
            HabitLog.tracked_habit_id == habit.id,
            db.func.date(HabitLog.date_logged).between(current_week[0], current_week[1])
        ).count()
        if logs_this_week < habit.goal.goal_freq:
            habits_to_remind.append(habit.habit_name)
    return habits_to_remind

def send_reminder_email(user, habits_to_remind):
    habit_list = "\n".join(habits_to_remind)
    subject = "Reminder: Habit Tracking for Today"
    body = f"""
    Hi {user.username},

    This is a reminder to complete your habits for today. Here are the habits you're still working on:

    {habit_list}

    Keep going! You're doing great.

    Best,
    Daily Sync
    """
    msg = Message(subject, recipients=[user.email], body=body)
    mail.send(msg)

def send_daily_reminder():
    with current_app.app_context():
        users = User.query.all()
        for user in users:
            habits_to_remind = generate_habits_to_remind(user)
            if habits_to_remind:
                send_reminder_email(user, habits_to_remind)
