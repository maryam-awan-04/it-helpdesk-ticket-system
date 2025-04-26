"""
Admin routes for the application
"""

from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboards/admin.html")
