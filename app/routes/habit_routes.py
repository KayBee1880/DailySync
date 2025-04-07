
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Habit, TrackedHabit, HabitLog, Goal
from extensions import db
from datetime import datetime

habits_bp = Blueprint('habits', __name__)

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
