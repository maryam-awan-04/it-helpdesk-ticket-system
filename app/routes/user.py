"""
User routes for the application
"""

from flask import Blueprint, render_template

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboards/user.html")
