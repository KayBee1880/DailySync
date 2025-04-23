from flask import Blueprint, request, jsonify, flash, url_for, redirect, render_template, current_app
from flask_login import login_required, current_user
from models import Habit, TrackedHabit, HabitLog, Goal
from extensions import db, mail
from datetime import datetime, timezone, date, timedelta
from support import get_weekly_logs, get_monthly_logs

habits_bp = Blueprint('habits', __name__)


@habits_bp.route("/add-habit", methods=['GET', 'POST'])
@login_required
def add_habit():
    try:
        if request.method == 'GET':
            return render_template('dashboard-2.html')

        habit_name = request.form.get('habit', '').strip()
        goal_type = request.form.get('goal_type')
        
        if habit_name != 'Custom':
            habit = Habit.query.filter_by(name=habit_name).first()

            if not habit:
                flash('Habit does not exist', 'error')
                return redirect(url_for('auth.dashboard'))
            

            if TrackedHabit.query.filter_by(habit_id=habit.id).first():
                flash('This habit is already being tracked', 'error')
                return redirect(url_for('auth.dashboard'))
                
            new_tracked_habit = TrackedHabit(user_id=current_user.id, habit_name=habit_name, habit_id=habit.id)

        elif habit_name == 'Custom':
            custom_name = request.form.get("custom_name")
            custom_description = request.form.get("custom_description")

            if not custom_name or len(custom_name.strip()) == 0:
                flash('Please provide a valid name for the custom habit.', 'error')
                return redirect(url_for('auth.dashboard'))
            
            normalized_name = custom_name.strip().lower()
            if Habit.query.filter(db.func.lower(Habit.name) == normalized_name).first():
                flash('A predefined habit by this name is already provided', 'error')
                return redirect(url_for('auth.dashboard'))   
            
            if TrackedHabit.query.filter_by(habit_name=custom_name).first():
                flash('A custom habit by this name is already being tracked', 'error')
                return redirect(url_for('auth.dashboard'))
            
            custom_habit = Habit(name=custom_name,category='Custom',description=custom_description)  # assuming you have an is_custom field; optional
            db.session.add(custom_habit)
            db.session.flush() 
  

            new_tracked_habit = TrackedHabit(user_id=current_user.id, habit_name=custom_name, habit_id=custom_habit.id)

        db.session.add(new_tracked_habit)
        db.session.commit()
        if goal_type == 'daily':
            goal_freq = 7  # Daily goal is always 7 (one for each day of the week)
        elif goal_type == 'weekly':
            goal_freq = request.form.get('goal_frequency', type=int)
            if not goal_freq:
                flash('Please provide a valid goal frequency for weekly goal', 'error')
                return redirect(url_for('auth.dashboard'))
        elif goal_type == 'monthly':
            raw_monthly_freq = request.form.get('goal_frequency', type=int)
            goal_freq = max(raw_monthly_freq // 4, 1)  # Ensures at least 1
            if not goal_freq:
                flash('Please provide a valid goal frequency for monthly goal', 'error')
                return redirect(url_for('auth.dashboard'))

        new_goal = Goal(user_id=current_user.id, tracked_habit_id=new_tracked_habit.id,
                        goal_freq=goal_freq, goal_type=goal_type)
        
        print('New goal',new_goal)
        db.session.add(new_goal)
        db.session.commit()
        flash('Habit added successfully','success')
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
        print(url_for('habits.edit_habit'))
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
        

        # Check if already logged today
        existing_log = HabitLog.query.filter(
            HabitLog.tracked_habit_id == habit_id,
            db.func.date(HabitLog.date_logged) == date.today()
        ).first()

        if existing_log:
            flash('This habit has already been logged today.', 'info')
            return redirect(url_for('auth.dashboard'))
    
        #create habit log
        new_log = HabitLog(tracked_habit_id=habit_id,date_logged=datetime.now(timezone.utc),completed=True)
        db.session.add(new_log)

        
        #update habit streak
        tracked_habit = TrackedHabit.query.get(habit_id)
        tracked_habit.last_completed = new_log.date_logged
        yesterday = date.today() - timedelta(days=1)

        yesterday_log = HabitLog.query.filter(
            HabitLog.tracked_habit_id == habit_id,
            db.func.date(HabitLog.date_logged) == yesterday
        ).first()

        if yesterday_log:
            tracked_habit.streak += 1
        else:
            tracked_habit.streak = 1

        db.session.commit()
        flash(f'{tracked_habit.habit_name} has been logged successfully','success')
        return redirect(url_for('auth.dashboard'))      


    except Exception as e:
        db.session.rollback()
        flash(f'Error viewing habits: {e}', 'error')
        return redirect(url_for('auth.dashboard'))

@habits_bp.route("/undo-habit", methods=["POST"])
@login_required
def undo_habit():
    habit_id = request.form.get("habit_id")
    today = date.today()

    try:
        log = HabitLog.query.filter(HabitLog.tracked_habit_id == int(habit_id), db.func.date(HabitLog.date_logged) == today).first()
        print(log,"today",today)
        if log:
            habit = TrackedHabit.query.get(habit_id)
            habit.streak = max(habit.streak - 1,0)
            db.session.delete(log)
            db.session.commit()
            flash("Habit log undone for today.", "success")
        else:
            flash("No log found for today to undo.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Error undoing habit: {e}", "error")

    return redirect(url_for("auth.dashboard"))


@habits_bp.route("/edit-habit", methods=['POST'])
@login_required
def edit_habit():
    try:
        habit_id = request.form.get("habit_id")
        goal_type = request.form.get("goal_type")
        goal_freq = request.form.get("goal_frequency")


        goal = Goal.query.join(TrackedHabit).filter(
            Goal.tracked_habit_id == habit_id,
            TrackedHabit.user_id == current_user.id
        ).first()
        goal.goal_type = goal_type
        if goal_type == 'daily':
            goal.goal_freq = 7  # Daily goal is always 7 (one for each day of the week)
        elif goal_type == 'weekly':
            goal.goal_freq = request.form.get('goal_frequency', type=int)
            if not goal_freq:
                flash('Please provide a valid goal frequency for weekly goal', 'error')
                return redirect(url_for('auth.dashboard'))
        elif goal_type == 'monthly':
            raw_monthly_freq = request.form.get('goal_frequency', type=int)
            goal.goal_freq = max(raw_monthly_freq // 4, 1)  # Ensures at least 1
            if not goal_freq:
                flash('Please provide a valid goal frequency for monthly goal', 'error')
                return redirect(url_for('habits.get_habits'))

        db.session.commit()
        flash('Successfully edited habit.', 'success')
        return redirect(url_for('habits.get_habits'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error editing habit: {e}', 'error')
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
        feedback = []
        habit_labels = []
        habit_labels_month = []
        last_week_data = []
        current_week_data = []
        last_month_data = []
        this_month_data = []
        for habit in current_user.tracked_habits:
            print(habit.habit_name)
            print(habit.goal)

            current_week, last_week = get_weekly_logs()
            last_month, this_month = get_monthly_logs()
            logs_this_week =  HabitLog.query.filter(
                    HabitLog.tracked_habit_id == habit.id,
                    db.func.date(HabitLog.date_logged).between(current_week[0], current_week[1])
                ).count()
            print("Expected range for last week:", last_week[0], "-", last_week[1])
            logs_last_week =  HabitLog.query.filter(
                    HabitLog.tracked_habit_id == habit.id,
                    db.func.date(HabitLog.date_logged).between(last_week[0], last_week[1])
                ).count()
            
            logs_this_month = HabitLog.query.filter(
                HabitLog.tracked_habit_id == habit.id,
                db.func.date(HabitLog.date_logged).between(this_month[0], this_month[1])
            ).count()

            logs_last_month = HabitLog.query.filter(
                HabitLog.tracked_habit_id == habit.id,
                db.func.date(HabitLog.date_logged).between(last_month[0], last_month[1])
            ).count()
            
            last_week_data.append(logs_last_week)
            current_week_data.append(logs_this_week)
            last_month_data.append(logs_last_month)
            this_month_data.append(logs_this_month)
            habit_labels.append(habit.habit_name)
            habit_labels_month.append(habit.habit_name)


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
                feedback.append((f'Congrats! You\'ve fulfilled your commitment to your {habit.habit_name} habit this week','positive'))
            elif habit.goal.goal_freq < logs_this_week:
                feedback.append((f'Well done! You\'ve exceeded your goal for your {habit.habit_name} habit this week','positive'))


        return render_template(
            'user-progress.html',
            comments = feedback,
            user=current_user,
            habits = current_user.tracked_habits,
            habit_labels=habit_labels,
            habit_labels_month=habit_labels_month,
            last_week_data=last_week_data,
            current_week_data=current_week_data,
            last_month_data=last_month_data,
            this_month_data=this_month_data,
            )
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading progress habit: {e}', 'error')
        return redirect(url_for('auth.dashboard'))
    