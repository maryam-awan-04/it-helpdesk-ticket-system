"""
Admin routes for the application
"""

from flask import Blueprint, redirect, render_template, session, url_for

from app.forms.registration import RegistrationForm
from app.forms.ticket import TicketForm

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    from app.models import Ticket, User

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    # Retrieve all tickets
    all_tickets = Ticket.query.all()

    # Retrieve tickets by status for dashboard summary
    assigned_tickets = [t for t in all_tickets if t.assigned_to == user.id]
    in_progress_tickets = [t for t in all_tickets if t.assigned_to == user.id]
    unassigned_tickets = [
        t for t in all_tickets if t.status == "Open" and t.assigned_to is None
    ]

    return render_template(
        "admin/dashboard.html",
        user=user,
        assigned_tickets=assigned_tickets,
        in_progress_tickets=in_progress_tickets,
        unassigned_tickets=unassigned_tickets,
    )


@bp.route("/manage-tickets", methods=["GET", "POST"])
def manage_tickets():
    from app.models import Ticket, User

    form = TicketForm()

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    # Retrieve all tickets
    all_tickets = Ticket.query.all()

    if form.validate_on_submit():
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/manage_tickets.html", form=form, user=user, all_tickets=all_tickets
    )


@bp.route("/manage-users", methods=["GET", "POST"])
def manage_users():
    from app.models import User

    form = RegistrationForm()

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    if form.validate_on_submit():
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/manage_users.html", form=form, user=user)
