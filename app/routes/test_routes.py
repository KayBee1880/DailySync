from flask import render_template, Blueprint

test_bp = Blueprint("test", __name__)

@test_bp.route("/test", methods=['GET'])
def test_page():
    return render_template("dashboard-2.html")

@test_bp.route("/test-setup", methods=['GET'])
def test_setup():
    return render_template("setup.html")

@test_bp.route("/test-habits", methods=['GET'])
def test_habits():
    return render_template("habits.html")

@test_bp.route("/test-signup", methods=['GET'])
def test_signup():
    return render_template("signup.html")

@test_bp.route("/test-signup", methods=['GET'])
def test_settings():
    return render_template("updated-settings.html")