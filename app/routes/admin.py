"""
Admin routes for the application
"""

from flask import Blueprint, redirect, render_template, url_for

from app.forms.registration import RegistrationForm
from app.forms.ticket import TicketForm

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("admin/dashboard.html")


@bp.route("/manage-tickets", methods=["GET", "POST"])
def manage_tickets():

    form = TicketForm()

    if form.validate_on_submit():
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/manage_tickets.html", form=form)


@bp.route("/manage-users", methods=["GET", "POST"])
def manage_users():

    form = RegistrationForm()

    if form.validate_on_submit():
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/manage_users.html", form=form)
