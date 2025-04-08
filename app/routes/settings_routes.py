from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, logout_user
from models import User
from extensions import db

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/user-settings", methods=['GET'])
@login_required
def user_settings():
    return render_template("settings.html")

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

@settings_bp.route("/change_username", methods=['POST'])
@login_required
def change_username():
    data = request.json
    user = User.query.get(current_user.id)
    
    if User.query.filter_by(username=data["new_username"]).first():
        return jsonify({"error": "Username already taken"}), 400
    
    user.username = data["new_username"]
    db.session.commit()
    return jsonify({"message": "Username changed successfully"}), 200

@settings_bp.route("/account_info", methods=['GET'])
@login_required
def account_info():
    user = User.query.get(current_user.id)
    return jsonify({
        "username": user.username,
        "joined_date": user.joined_date.strftime("%Y-%m-%d")  # assuming you have this field
    }), 200

