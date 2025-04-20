from flask import Blueprint, request, jsonify, flash, url_for, redirect, render_template
from flask_login import login_required, current_user
from models import Habit, TrackedHabit, HabitLog, Goal
from extensions import db
from datetime import datetime, timezone
from support import get_weekly_logs

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
        if not goal_type == 'daily':
            goal_freq = request.form.get("goal_frequency")
        else:
            goal_freq = 365
        new_goal = Goal(user_id=current_user.id, tracked_habit_id=new_tracked_habit.id,
                        goal_freq=goal_freq, goal_type=goal_type)
        print('New goal',new_goal)
        db.session.add(new_goal)
        db.session.commit()

        return redirect(url_for('auth.dashboard'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error adding new habit: {e}', 'error')
        return redirect(url_for('auth.dashboard'))


@habits_bp.route("/view-habits", methods=['GET'])
@login_required
def get_habits():
    try:
        user = current_user
        return render_template('view-habits.html',user=current_user, habits=user.tracked_habits,all_habits = Habit.query.all())
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error viewing habits: {e}', 'error')
        return redirect(url_for('auth.dashboard'))


@habits_bp.route("/log-habit", methods=['POST'])
@login_required
def log_habit():
    try:
        #retrieve habit id from html form
        habit_id = request.form.get("habit_id")
        if not habit_id:
            flash('No habit id provided','error')
            return redirect(url_for('auth.dashboard'))
    
        #create habit log
        new_log = HabitLog(tracked_habit_id=habit_id,date_logged=datetime.now(timezone.utc),completed=True)
        db.session.add(new_log)

        #update habit streak
        tracked_habit = TrackedHabit.query.get(habit_id)
        tracked_habit.last_completed = new_log.date_logged
        tracked_habit.streak += 1

        db.session.commit()
        flash(f'{tracked_habit.habit_name} has been logged successfully','success')
        return redirect(url_for('auth.dashboard'))      


    except Exception as e:
        db.session.rollback()
        flash(f'Error viewing habits: {e}', 'error')
        return redirect(url_for('auth.dashboard'))



@habits_bp.route("/edit-habit", methods=['POST'])
@login_required
def edit_habit():
    try:
        if request.method == 'POST':
            goal = Goal.query.filter_by(tracked_habit_id = request.form.get("habit_id")).first()
            goal.goal_type = request.form.get("goal_type")
            if not goal.goal_type == 'daily':
                goal.goal_freq = request.form.get("goal_frequency")
            else:
                goal.goal_freq = 365

            db.session.commit()
            flash(f'Successfully edited habit','success')
            return redirect(url_for('habits.get_habits'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error viewing habits: {e}', 'error')
        return redirect(url_for('habits.get_habits'))


@habits_bp.route("/delete-habit", methods=['POST'])
@login_required
def delete_habit():
    try:
        habit_id = request.form.get("habit_id")
        habit = TrackedHabit.query.filter_by(id=habit_id, user_id=current_user.id).first()
        if habit:
            db.session.delete(habit)
            db.session.commit()
            flash(f'Successully deleted habit {habit_id}','success')
            return redirect(url_for('habits.get_habits'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting habit: {e}', 'error')
        return redirect(url_for('habits.get_habits'))


@habits_bp.route("/progress", methods = ['GET'])
@login_required
def user_progress():
    feedback = ["First comment","Second comment","Third comment"]
    for habit in current_user.tracked_habits:
        print(habit.habit_name)
        print(habit.goal)
        #current_week, last_week = get_weekly_logs(habit.id)
        current_week, last_week = 2,1
        percent_change = abs(round(((current_week - last_week)/last_week) * 100))
        if current_week > last_week:
            feedback.append(f'Congrats! Your commitment to your {habit.habit_name} habit is up {percent_change}% this week')
        elif current_week < last_week:
            feedback.append(f'Your {habit.habit_name} logs was down {percent_change}% this week. Consider lowering your goal \
                             to a more comfortable frequency then progressively increase.')
        
        if habit.goal.goal_freq == current_week:
            feedback.append(f'Congrats! You fulfilled your commitment to your {habit.habit_name} habit this week')
            
    return render_template('user-progress.html', comments = feedback, user=current_user, habits = current_user.tracked_habits)
