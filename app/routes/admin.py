"""
Admin routes for the application
"""

from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from app.forms.ticket import UpdateTicketForm
from app.forms.user import UserForm

bp = Blueprint("admin", __name__, url_prefix="/admin")

STATUS_OPTIONS = ["Open", "In Progress", "On Hold", "Resolved", "Closed"]
REQUEST_TYPE_OPTIONS = [
    "Access Request",
    "Hardware Issue",
    "Software Issue",
    "Network Issue",
    "Security Incident",
    "Service Request",
    "Onboarding Request",
    "Offboarding Request",
    "Other",
]


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    from app.models import Ticket, User

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()
    all_tickets = Ticket.query.all()

    # Get filters from query parameters
    status_filter = request.args.getlist("status")
    type_filter = request.args.getlist("request_type")

    # Apply filters
    assigned_tickets = [
        t
        for t in all_tickets
        if t.assigned_to == user.id
        and (not status_filter or t.status in status_filter)
        and (not type_filter or t.request_type in type_filter)
    ]

    unassigned_tickets = [
        t
        for t in all_tickets
        if t.status == "Open"
        and t.assigned_to is None
        and (not type_filter or t.request_type in type_filter)
    ]

    return render_template(
        "admin/dashboard.html",
        user=user,
        assigned_tickets=assigned_tickets,
        unassigned_tickets=unassigned_tickets,
        status_options=STATUS_OPTIONS,
        request_type_options=REQUEST_TYPE_OPTIONS,
    )


@bp.route("/manage-tickets", methods=["GET", "POST"])
def manage_tickets():
    from app import db
    from app.models import Ticket, User

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    # Get filters from query parameters
    status_filter = request.args.getlist("status")
    type_filter = request.args.getlist("request_type")
    assigned_to_filter = request.args.get("assigned_to")
    creator_user_filter = request.args.get("creator_user")

    # Apply filters
    all_tickets = Ticket.query.all()
    filtered_tickets = [
        t
        for t in all_tickets
        if (not status_filter or t.status in status_filter)
        and (not type_filter or t.request_type in type_filter)
        and (
            not assigned_to_filter
            or (t.assigned_to and str(t.assigned_to) == assigned_to_filter)
        )
        and (
            not creator_user_filter
            or (t.creator_user and str(t.creator_user.id) == creator_user_filter)
        )
    ]

    if "delete_ticket" in request.form:
        # Retrieve ticket from the database
        ticket_id = request.form.get("delete_ticket_id")
        delete_ticket = Ticket.query.get(ticket_id)

        # Delete ticket from the database
        db.session.delete(delete_ticket)
        db.session.commit()

        flash("Ticket deleted successfully.", "success")
        return redirect(url_for("admin.manage_tickets"))

    admins = User.query.filter_by(role="Admin").all()
    all_admins = [(admin.id, f"{admin.firstname} {admin.surname}") for admin in admins]
    creators = User.query.filter(
        User.id.in_(
            [t.creator_user.id for t in all_tickets if t.creator_user is not None]
        )
    ).all()
    all_creators = [
        (creator.id, f"{creator.firstname} {creator.surname}") for creator in creators
    ]

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
        all_tickets=filtered_tickets,
        show_edit_popup=show_edit_popup,
        status_options=STATUS_OPTIONS,
        request_type_options=REQUEST_TYPE_OPTIONS,
        all_admins=all_admins,
        all_creators=all_creators,
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
