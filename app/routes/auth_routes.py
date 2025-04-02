from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from models import User
from extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register",methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data["password"], method ="pbkdf2:sha256")

    new_user = User(username=data["username"],password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User registered successfully"}),201


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