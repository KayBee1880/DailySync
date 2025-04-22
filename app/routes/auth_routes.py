from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from models import User, Habit, TrackedHabit, HabitLog
from extensions import db, bcrypt
from support import validate_password, get_week_range, get_current_week_dates, get_local_today
from datetime import datetime, timezone, date

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=['GET'])
def index():
    return redirect(url_for('auth.login'))

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
            flash('User account created successfully','success')
            return redirect(url_for('auth.login'))
            #return jsonify({"message":"User registered successfully"}),201
    except Exception as e:
        db.session.rollback()
        flash(f'Error registering user: {e}','error')
        return redirect(url_for('auth.register'))

@auth_bp.route("/login", methods=['GET','POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('login.html',user=current_user)
        elif request.method == 'POST':
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and bcrypt.check_password_hash(user.password,request.form.get('password')):
                login_user(user)
                flash(f'User {user.username} successfully logged in','success')
                return redirect(url_for('auth.dashboard'))
            elif not user:
                flash('No such account exists','error')
                return redirect(url_for('auth.register'))
            else:
                print(request.form.get('username'), user.username)
                flash('Invalid username or password','error')
                return redirect(url_for('auth.login'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error logging in user: {e}','error')
        return redirect(url_for('auth.login'))

@auth_bp.route("/user-dashboard",methods=['GET','POST'])
@login_required
def dashboard():
    try:
        week_offset = int(request.args.get('week_offset',0))
        today = get_local_today()
        week_range = get_week_range(week_offset)
        week_dates = get_current_week_dates(week_offset)
        week_dates_only = [d.date() for d in week_dates]
        user = current_user

        all_logs_today = [] #what habits were ogged today for today panel
        logs_by_habit = {} #what date of the week was a habit logged

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
                log.date_logged.date().isoformat(): log for log in logs_this_week
            }
            for log in habit.logs:
                if log.date_logged.date() == today:
                    all_logs_today.append(habit.id)
                    break
        print(f"Today: {today}")                
        print(f"Logged today: ",all_logs_today)
        print("Week range:", get_week_range())
        print("Dates:", get_current_week_dates())
        print("Logs by habit",logs_by_habit)

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
                logs_by_habit = logs_by_habit
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




"""
/register , methods = [POST]
This handler function will add a new user to the database

/login , methods = [POST]
This handler function will authenticate an existing user using Flask’s login manager object.

/habits , methods = [GET]
This handler function will retrieve the user’s tracked habits from the database

/track-habit , methods = [POST]
This handler function will add a new tracked habit for the user.

/log-habit , methods = [POST]
This handler function will store whether or not the user completed their tracked habit

/progress , methods = [GET]
This handler function will retrieve the user’s habit log history for each tracked habit.
/set-goal , methods = [POST]
This handler function will allow users to create a new goal for a habit or edit an existing goal.

/remove-habit/<habit_id> , methods = [DEETE]
This handler function will add a new user to the database

/report , methods = [GET]
This handler function will generate progress reports for the user over a chosen tie interval. The reports will also include feedback based on the user’s performance with each habit.
"""