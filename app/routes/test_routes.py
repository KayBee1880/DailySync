from flask import render_template, Blueprint

test_bp = Blueprint("test", __name__)

@test_bp.route("/test", methods=['GET'])
def test_page():
    return render_template("dashboard-2.html")