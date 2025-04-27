"""
User routes for the application
"""

from flask import Blueprint, redirect, render_template, url_for

from app.forms.create_ticket import CreateTicket

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("user/dashboard.html")


@bp.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():

    form = CreateTicket()

    if form.validate_on_submit():
        return redirect(url_for("user.dashboard"))

    return render_template("user/create_ticket.html", form=form)
