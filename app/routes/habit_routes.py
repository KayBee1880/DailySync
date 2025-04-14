from flask import Blueprint, request, jsonify, flash, url_for, redirect, render_template
from flask_login import login_required, current_user
from models import Habit, TrackedHabit, HabitLog, Goal
from extensions import db
from datetime import datetime

habits_bp = Blueprint('habits', __name__)


@habits_bp.route("/add-habit", methods=['GET', 'POST'])
@login_required
def add_habit():
    try:
        if request.method == 'GET':
            return render_template('dashboard-2.html')

        habit_name = request.form.get('habit')
        goal_freq = request.form.get('goal_frequency')
        goal_type = request.form.get('goal_type')

        habit = Habit.query.filter_by(name=habit_name).first()
        if not habit:
            flash('Habit does not exist', 'error')
            return redirect(url_for('auth.dashboard'))

        new_tracked_habit = TrackedHabit(user_id=current_user.id, habit_name=habit_name, habit_id=habit.id)
        db.session.add(new_tracked_habit)
        db.session.commit()

        new_goal = Goal(user_id=current_user.id, tracked_habit_id=new_tracked_habit.id,
                        goal_freq=goal_freq, goal_type=goal_type)
        db.session.add(new_goal)
        db.session.commit()

        return redirect(url_for('auth.dashboard'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error adding new habit: {e}', 'error')
        return redirect(url_for('auth.dashboard'))


@habits_bp.route("/habits", methods=['GET'])
@login_required
def get_habits():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": h.id, "name": h.name} for h in habits]), 200


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
    return jsonify([{"habit_id": log.habit_id, "completed": log.completed, "date": log.date} for log in logs]), 200


@habits_bp.route("/set-goal", methods=['POST'])
@login_required
def set_goal():
    data = request.json
    goal = Goal.query.filter_by(tracked_habit_id=data["tracked_habit_id"]).first()
    if goal:
        goal.target = data["target"]
    else:
        goal = Goal(tracked_habit_id=data["tracked_habit_id"], target=data["target"])
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
        return jsonify({"message": "Habit removed successfully"}), 200
    return jsonify({"error": "Habit not found"}), 404


@habits_bp.route("/rename-habit/<int:habit_id>", methods=['PUT'])
@login_required
def rename_habit(habit_id):
    data = request.json
    new_name = data.get("new_name")

    if not new_name:
        return jsonify({"error": "New habit name is required"}), 400

    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    if habit:
        habit.name = new_name
        db.session.commit()
        return jsonify({"message": "Habit renamed successfully"}), 200

    return jsonify({"error": "Habit not found"}), 404


@habits_bp.route("/create-goal", methods=['POST'])
@login_required
def create_goal():
    data = request.json
    tracked_habit_id = data.get("tracked_habit_id")
    goal_freq = data.get("goal_freq")
    goal_type = data.get("goal_type")

    if not tracked_habit_id or not goal_freq or not goal_type:
        return jsonify({"error": "Missing required fields"}), 400

    existing_goal = Goal.query.filter_by(tracked_habit_id=tracked_habit_id, user_id=current_user.id).first()
    if existing_goal:
        return jsonify({"error": "Goal already exists for this habit"}), 400

    new_goal = Goal(
        user_id=current_user.id,
        tracked_habit_id=tracked_habit_id,
        goal_freq=goal_freq,
        goal_type=goal_type
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"message": "Goal created successfully"}), 201


@habits_bp.route("/report", methods=['GET'])
@login_required
def generate_report():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    report = {h.name: HabitLog.query.filter_by(habit_id=h.id).count() for h in habits}
    return jsonify(report), 200
