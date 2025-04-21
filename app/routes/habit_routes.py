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
        #how many times a week should they log a habit
        if goal_type == 'daily':
            goal_freq = 7
        elif goal_type == 'weekly':
            goal_freq = goal_freq
        elif goal_type == 'monthly':
            goal_freq = goal_freq // 4

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
    try:
        feedback = [("Feedback 1","negative"),("Feedback 2","negative")]
        habit_labels = []
        last_week_data = []
        current_week_data = []
        for habit in current_user.tracked_habits:
            print(habit.habit_name)
            print(habit.goal)

            current_week, last_week = get_weekly_logs()
            logs_this_week =  HabitLog.query.filter(
                    HabitLog.tracked_habit_id == habit.id,
                    db.func.date(HabitLog.date_logged).between(current_week[0], current_week[1])
                ).count()
            print("Expected range for last week:", last_week[0], "-", last_week[1])
            logs_last_week =  HabitLog.query.filter(
                    HabitLog.tracked_habit_id == habit.id,
                    db.func.date(HabitLog.date_logged).between(last_week[0], last_week[1])
                ).count()
            
            last_week_data.append(logs_last_week)
            current_week_data.append(logs_this_week)
            habit_labels.append(habit.habit_name)
            if logs_last_week == 0 and logs_this_week > 0:
                percent_change = 100
            elif logs_last_week == 0 and logs_this_week == 0:
                percent_change = 0
            elif logs_last_week != 0:
                percent_change = abs(round(((logs_this_week - logs_last_week)/logs_last_week) * 100))


            if logs_this_week > logs_last_week:
                feedback.append((f'Congrats! Your commitment to your {habit.habit_name} habit is up {percent_change}% this week','positive'))
            elif logs_this_week < logs_last_week:
                feedback.append((f'Your {habit.habit_name} logs was down {percent_change}% this week. Consider lowering your goal \
                                to a more comfortable frequency then progressively increase.','negative'))
            
            print(f"{habit.habit_name}: {habit.goal.goal_freq} and Current week {logs_this_week}")
            if habit.goal.goal_freq == logs_this_week:
                print('Goal freq',habit.goal.goal_freq,'Log this week', logs_this_week)
                feedback.append((f'Congrats! You\'ve fulfilled your commitment to your {habit.habit_name} habit this week','positive'))
            elif habit.goal.goal_freq < logs_this_week:
                feedback.append((f'Well done! You\'ve exceeded your goal for your {habit.habit_name} habit this week','positive'))

        return render_template(
            'user-progress.html',
            comments = feedback,
            user=current_user,
            habits = current_user.tracked_habits,
            habit_labels=habit_labels,
            last_week_data=last_week_data,
            current_week_data=current_week_data
            )
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading progress habit: {e}', 'error')
        return redirect(url_for('auth.dashboard'))