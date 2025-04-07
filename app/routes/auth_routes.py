from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from models import User
from extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@auth_bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
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


settings_bp = Blueprint("settings", __name__)

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

@settings_bp.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

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