from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from models import User, Habit, TrackedHabit
from extensions import db, bcrypt
from support import validate_password, get_week_range
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@auth_bp.route("/register",methods=['GET','POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template('register.html')
        
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
            return render_template('login.html')
        elif request.method == 'POST':
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and bcrypt.check_password_hash(user.password,request.form.get('password')):
                login_user(user)
                flash(f'User {user.username} successfully logged in','success')
                return redirect(url_for('auth.dashboard'))
            else:
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
        today = datetime.today()
        week_range = get_week_range()
        user = current_user
        for habit in user.tracked_habits:
            habit_completed = habit.last_completed == today
            habit.completed_today = habit_completed

        if request.method == 'GET':
            return render_template('dashboard-2.html',user=current_user,habits=user.tracked_habits,
                                    all_habits = Habit.query.all(),today_date = today, week_range=week_range)
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