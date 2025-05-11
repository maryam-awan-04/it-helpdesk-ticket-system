"""
Admin routes for the application
"""

from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from app.forms.ticket import UpdateTicketForm
from app.forms.user import UserForm

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
    from app import db
    from app.models import Ticket, User

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    # Retrieve all tickets
    all_tickets = Ticket.query.all()

    if "delete_ticket" in request.form:
        # Retrieve ticket from the database
        ticket_id = request.form.get("delete_ticket_id")
        delete_ticket = Ticket.query.get(ticket_id)

        # Delete ticket from the database
        db.session.delete(delete_ticket)
        db.session.commit()

        flash("Ticket deleted successfully.", "success")
        return redirect(url_for("admin.manage_tickets"))

    # Get admins to assign tickets
    admins = User.query.filter_by(role="Admin").all()
    all_admins = [(admin.id, f"{admin.firstname} {admin.surname}") for admin in admins]

    form = UpdateTicketForm()
    form.assigned_to.choices = [("", "Select an admin")] + all_admins
    show_edit_popup = False

    if form.validate_on_submit():
        # Retrieve ticket from the database
        ticket_id = form.id.data
        update_ticket = Ticket.query.get(ticket_id)

        # Update ticket details
        update_ticket.request_type = form.request_type.data
        update_ticket.title = form.title.data
        update_ticket.description = form.description.data
        update_ticket.status = form.status.data
        update_ticket.assigned_to = form.assigned_to.data
        if form.status.data == "Resolved":
            update_ticket.date_resolved = datetime.now().date()

        db.session.commit()
        flash("Ticket details updated successfully.", "success")

    elif request.method == "POST":
        show_edit_popup = True

    return render_template(
        "admin/manage_tickets.html",
        form=form,
        user=user,
        all_tickets=all_tickets,
        show_edit_popup=show_edit_popup,
    )


@bp.route("/manage-users", methods=["GET", "POST"])
def manage_users():
    from app import db
    from app.models import User

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    # Retrieve all users
    all_users = User.query.all()

    if "delete_user" in request.form:
        # Retrieve user from the database
        user_id = request.form.get("delete_user_id")
        delete_user = User.query.get(user_id)

        # Delete user from the database
        db.session.delete(delete_user)
        db.session.commit()

        flash("User deleted successfully.", "success")
        return redirect(url_for("admin.manage_users"))

    form = UserForm()

    if form.validate_on_submit():
        # Retrieve user from the database
        user_id = form.id.data
        update_user = User.query.get(user_id)

        # Update user details
        update_user.firstname = form.firstname.data
        update_user.surname = form.surname.data
        update_user.email = form.email.data
        update_user.role = form.role.data

        db.session.commit()

        flash("User details updated successfully.", "success")

    return render_template(
        "admin/manage_users.html", form=form, user=user, all_users=all_users
    )
