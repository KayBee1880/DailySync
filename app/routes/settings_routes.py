from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, logout_user
from models import User
from extensions import db

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
    data = request.json
    user = User.query.get(current_user.id)
    
    if not check_password_hash(user.password, data["current_password"]):
        return jsonify({"error": "Current password is incorrect"}), 400
    
    if data["new_password"] != data["confirm_password"]:
        return jsonify({"error": "New passwords don't match"}), 400
    
    user.password = generate_password_hash(data["new_password"], method="pbkdf2:sha256")
    db.session.commit()
    return jsonify({"message": "Password changed successfully"}), 200

@settings_bp.route('/update-user', methods=['POST'])
@login_required
def update_user():
    data = request.get_json()
    new_name = data.get('name')
    new_email = data.get('email')

    if not new_name or not new_email:
        return jsonify({'error': 'Missing fields'}), 400

    # Check if new email is already taken (by someone else)
    if new_email != current_user.email:
        existing = User.query.filter_by(email=new_email).first()
        if existing:
            return jsonify({'error': 'Email already in use'}), 400

    # Update fields
    current_user.name = new_name
    current_user.email = new_email
    db.session.commit()

    return jsonify({'message': 'User updated successfully', 'user': {
        'name': current_user.name,
        'email': current_user.email
    }}), 200

@settings_bp.route("/account_info", methods=['GET'])
@login_required
def account_info():
    user = User.query.get(current_user.id)
    return jsonify({
        "username": user.username,
        "joined_date": user.joined_date.strftime("%Y-%m-%d")  # assuming you have this field
    }), 200

