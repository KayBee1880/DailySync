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