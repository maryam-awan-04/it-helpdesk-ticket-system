"""
User routes for the application
"""

from flask import Blueprint, redirect, render_template, url_for

from app.forms.ticket import Ticket

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("user/dashboard.html")


@bp.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():

    form = Ticket()

    if form.validate_on_submit():
        return redirect(url_for("user.dashboard"))

    return render_template("user/create_ticket.html", form=form)


@bp.route("/update-ticket", methods=["GET", "POST"])
def update_ticket():

    form = Ticket()

    if form.validate_on_submit():
        return redirect(url_for("user.dashboard"))

    return render_template("user/update_ticket.html", form=form)
