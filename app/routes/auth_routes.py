from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from models import User
from extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register",methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data["password"], method ="pbkdf2:sha256")

    new_user = User(username=data["username"],password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User registered successfully"}),201

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@habits_bp.route("/habits", methods=['GET'])
@login_required
def get_habits():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return jsonify([{ "id": h.id, "name": h.name } for h in habits]), 200

@habits_bp.route("/track-habit", methods=['POST'])
@login_required
def track_habit():
    data = request.json
    new_habit = Habit(name=data["name"], user_id=current_user.id)
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({"message": "Habit tracked successfully"}), 201

@habits_bp.route("/log-habit", methods=['POST'])
@login_required
def log_habit():
    data = request.json
    new_log = HabitLog(habit_id=data["habit_id"], user_id=current_user.id, completed=data["completed"])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"message": "Habit log recorded"}), 201

@habits_bp.route("/progress", methods=['GET'])
@login_required
def get_progress():
    logs = HabitLog.query.filter_by(user_id=current_user.id).all()
    return jsonify([{ "habit_id": log.habit_id, "completed": log.completed, "date": log.date } for log in logs]), 200

@habits_bp.route("/set-goal", methods=['POST'])
@login_required
def set_goal():
    data = request.json
    goal = Goal.query.filter_by(habit_id=data["habit_id"]).first()
    if goal:
        goal.target = data["target"]
    else:
        goal = Goal(habit_id=data["habit_id"], target=data["target"])
        db.session.add(goal)
    db.session.commit()
    return jsonify({"message": "Goal set successfully"}), 201

@habits_bp.route("/remove-habit/<int:habit_id>", methods=['DELETE'])
@login_required
def remove_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    if habit:
        db.session.delete(habit)
        db.session.commit()
        return jsonify({"message": "Habit removed"}), 200
    return jsonify({"error": "Habit not found"}), 404

@habits_bp.route("/report", methods=['GET'])
@login_required
def generate_report():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    report = {h.name: HabitLog.query.filter_by(habit_id=h.id).count() for h in habits}
    return jsonify(report), 200

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