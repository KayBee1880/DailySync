from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from models import User
from extensions import db, bcrypt
from support import validate_password

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/user-settings", methods=['GET'])
@login_required
def user_settings():
    try:
        if request.method == 'GET':
            return render_template("updated-settings.html",user=current_user)
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

@settings_bp.route('/update-user', methods=['POST'])
@login_required
def update_account():
    try:
        new_username = request.form.get('username')
        new_email = request.form.get("email")

        if not new_username or not new_email:
            flash('Fill both fields','warning')
            return redirect(request.url)

        #check if same username is entered
        if new_username == current_user.username:
            flash('You\'re already using this username','error')
            return redirect(url_for('settings.user_settings'))
        
        #check if username is taken
        if new_email != current_user.email:
            existing = User.query.filter_by(username=new_username).first()
            if existing:
                flash('That username is already taken!','error')
                return redirect(url_for('settings.user_settings'))

        # Check if new email is already taken (by someone else)
        if new_email != current_user.email:
            existing = User.query.filter_by(email=new_email).first()
            if existing:
                flash('That email is already taken!','error')
                return redirect(url_for('settings.user_settings'))
        elif new_email == current_user.email:
            flash('You\'re already using this email','error')
            return redirect(url_for('settings.user_settings'))
        
        # if checks passed update fields
        current_user.username = new_username
        current_user.email = new_email
        db.session.commit()

        flash('User updated successfully','success')
        return redirect(url_for('settings.user_settings'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading user settings: {e}')
        return redirect(url_for('settings.user_settings'))

@settings_bp.route("/account_info", methods=['GET'])
@login_required
def account_info():
    user = User.query.get(current_user.id)
    return jsonify({
        "username": user.username,
        "joined_date": user.joined_date.strftime("%Y-%m-%d")  # assuming you have this field
    }), 200

@settings_bp.route("/account_info", methods=['GET'])
@login_required
def reset_progress():
    user = User.query.get(current_user.id)
    return jsonify({
        "username": user.username,
        "joined_date": user.joined_date.strftime("%Y-%m-%d")  # assuming you have this field
    }), 200
