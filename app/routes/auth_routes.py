from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_mail import Mail, Message
from models import User, Habit, TrackedHabit, HabitLog
from extensions import db, bcrypt, mail
from support import validate_password, get_week_range, get_current_week_dates, get_local_today, validate_email,validate_username
from datetime import datetime, timezone, date

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=['GET'])
def index():
    try:
        return render_template('login.html')
    
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return "An error occurred", 500

@auth_bp.route("/register",methods=['GET','POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template('signup.html',user=current_user)
        
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2') 
        email = request.form.get('email')
        id = request.form.get("id")

        if not username or not password1 or not password2 or not email: #check if all fields are filled in form
            flash('All fields are required','warning')
            return redirect(url_for('auth.register'))
        
        valid, message, category = validate_username(username) 
        if not valid and message:
            flash(message,category)
            return redirect(url_for('auth.register'))

        valid, message, category = validate_email(email) 
        if not valid and message:
            flash(message,category)
            return redirect(url_for('auth.register'))

        
        valid, message, category = validate_password(password1,password2) 
        if not valid and message: #validate password
            flash(message,category)
            return redirect(url_for('auth.register'))
        password = password1

        if User.query.filter_by(username=username).first(): #check if user already exists in User table
            flash('This username already exists!','error')
            return redirect(url_for('auth.register'))
        
        if username and password:

            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

            new_user = User(id=id,username=username,password = hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            send_confirmation_email(username,email)
            flash('User account created successfully','success')
            return redirect(url_for('auth.login'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error registering user: {e}','error')
        return redirect(url_for('auth.register'))
    
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('login.html')

        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash(f'User {user.username} successfully logged in', 'success')
                return redirect(url_for('auth.dashboard'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('No such account exists', 'error')
            return redirect(url_for('auth.register'))

        return redirect(url_for('auth.login'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error logging in user: {e}', 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route("/user-dashboard",methods=['GET','POST'])
@login_required
def dashboard():
    try:
        try:
            week_offset = int(request.args.get('week_offset', 0))
        except ValueError:
            flash('Invalid week offset value.', 'error')
            return redirect(url_for('auth.dashboard'))

        today = get_local_today()
        week_range = get_week_range(week_offset)
        week_dates = get_current_week_dates(week_offset)
        week_dates_only = [d.date() for d in week_dates]
        user = current_user

        all_logs_today = [] #what habits were ogged today for today panel
        logs_by_habit = {} #what date of the week was a habit logged
        logs_this_week = []

        for habit in user.tracked_habits:
            #get all user logs for this week
            logs =  HabitLog.query.filter(
                HabitLog.tracked_habit_id == habit.id,
                db.func.date(HabitLog.date_logged).between(week_dates_only[0], week_dates_only[-1])
                ).all()
            
            logs_this_week = [
                log for log in logs
                if log.date_logged.date() in week_dates_only
            ]

            logs_by_habit[habit.id] = {
                "logs": {log.date_logged.date().isoformat(): log for log in logs_this_week},
                "count": len(logs_this_week)
            }
            for log in habit.logs:
                if log.date_logged.date() == today:
                    all_logs_today.append(habit.id)
                    break

        if request.method == 'GET':
            return render_template(
                'dashboard-2.html',
                user=current_user,
                habits=user.tracked_habits,
                all_habits = Habit.query.all(),
                today_date = today,
                week_range=week_range,
                week_offset=week_offset,
                logged_today = all_logs_today,
                week_dates=week_dates,
                logs_by_habit = logs_by_habit,
                num_of_logs = len(logs_this_week),
                )
        elif request.method == 'POST':
                return redirect(url_for('auth.dashboard'))

    except Exception as e:
        db.session.rollback()
        flash(f'error encountered: {e}','error')
        return redirect(url_for('auth.login'))

@auth_bp.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def send_confirmation_email(username, email):
    username = username
    email = email
    subject = "Welcome to Daily Sync"
    body = f"""
    Hello {username},

    Thank you for signing up for Daily Sync. We’re excited to have you on board!
    Let\'s start tracking!

    Best,
    Daily Sync
    """

    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)