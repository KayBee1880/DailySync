from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from models import User, TrackedHabit, HabitLog
from extensions import db, bcrypt
from support import validate_password, validate_email, validate_username

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/user-settings", methods=['GET'])
@login_required
def user_settings():
    try:
        if request.method == 'GET':
            return render_template("settings.html",user=current_user)
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading user settings: {e}')
        return redirect(url_for('auth.dashboard'))

@settings_bp.route("/change_password", methods=['POST'])
@login_required
def change_password():
    try:
        current_password = request.form.get("current_password")
        password1 = request.form.get("new_password")
        password2 = request.form.get("confirm_password")
        
        if not bcrypt.check_password_hash(current_user.password, current_password):
            flash('The password you entered is incorrect','error')
            return redirect(url_for('settings.user_settings'))
        
        valid, message, category = validate_password(password1,password2)
        if not valid:
            flash(message,category)
            return redirect(url_for('settings.user_settings'))
        
        if password1 == current_password:
            flash('You cannot change to your current password!','error')
            return redirect(url_for('settings.user_settings'))

        current_user.password = bcrypt.generate_password_hash(password1).decode("utf-8")
        db.session.commit()
        flash('Password changed successfully','success')
        return redirect(url_for('settings.user_settings'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading user settings: {e}')
        return redirect(url_for('auth.dashboard'))

@settings_bp.route('/update-username', methods=['POST'])
@login_required
def update_username():
    try:
        new_username = request.form.get('username')
        if not new_username:
            flash('Fill both fields','warning')
            return redirect(request.url)
        
        valid, message, category = validate_username(new_username) 
        if not valid and message:
            flash(message,category)
            return redirect(url_for('settings.user_settings'))

        #check if same username is entered and if username is taken
        if new_username == current_user.username:
            flash('You\'re already using this username','error')
            return redirect(url_for('settings.user_settings'))
        elif new_username != current_user.username:
            existing = User.query.filter_by(username=new_username).first()
            if existing:
                flash('That username is already taken!','error')
                return redirect(url_for('settings.user_settings'))
               
        
        # if checks passed update fields
        current_user.username = new_username
        db.session.commit()
        flash('User\'s account updated successfully','success')
        return redirect(url_for('settings.user_settings'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading user settings: {e}')
        return redirect(url_for('settings.user_settings'))

@settings_bp.route('/update-user-email', methods=['POST'])
@login_required
def update_email():
    try:
        new_email = request.form.get("email")

        if not new_email:
            flash('Fill the field','warning')
            return redirect(request.url)
        valid, message, category = validate_email(new_email) 
        if not valid and message:
            flash(message,category)
            return redirect(url_for('settings.user_settings'))

        # Check if new email is already taken (by someone else)
        if new_email != current_user.email:
            existing = User.query.filter_by(email=new_email).first()
            if existing:
                flash('That email is already taken!','error')
                return redirect(url_for('settings.user_settings'))
        else:
            flash('You\'re already using this email','error')
            return redirect(url_for('settings.user_settings'))
        
        # if checks passed update fields
        current_user.email = new_email  
        db.session.commit()
        flash('User\'s account updated successfully','success')
        return redirect(url_for('settings.user_settings'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading user settings: {e}')
        return redirect(url_for('settings.user_settings'))



@settings_bp.route("/reset-progress", methods=['POST'])
@login_required
def reset_progress():
    try:
        user_habits = TrackedHabit.query.filter_by(user_id=current_user.id).all()
        if user_habits:
            for habit in user_habits:
                HabitLog.query.filter_by(tracked_habit_id=habit.id).delete()
                db.session.delete(habit)
            db.session.commit()

            flash('Progress has been reset successfully','success')
            return redirect(url_for('settings.user_settings'))
        else:
            flash('There is no progress to reset','error')
            return redirect(url_for('settings.user_settings'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting user progress: {e}')
        return redirect(url_for('settings.user_settings'))
     
@settings_bp.route("/delete-account", methods=['POST'])
@login_required
def delete_account():
    try:
        user_habits = TrackedHabit.query.filter_by(user_id=current_user.id).all()
        if user_habits:
            for habit in user_habits:
                HabitLog.query.filter_by(tracked_habit_id=habit.id).delete()
                db.session.delete(habit)
                
        db.session.delete(current_user)
        db.session.commit()
        flash('account deleted successfully', 'success')
        return redirect(url_for('auth.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting user progress: {e}')
        return redirect(url_for('settings.user_settings'))