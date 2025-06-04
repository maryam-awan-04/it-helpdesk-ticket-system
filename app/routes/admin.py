"""
Admin routes for the application.
"""

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.ticket import UpdateTicketForm
from app.forms.user import UserForm
from app.routes.constants import REQUEST_TYPES, ROLES, STATUSES

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """
    Admin dashboard displaying assigned and unassigned tickets.
    """
    from app.models import Ticket

    all_tickets = Ticket.query.all()

    # Get filters
    status_filter = request.args.getlist("status")
    type_filter = request.args.getlist("request_type")

    # Filter tickets assigned to the current user
    assigned_tickets = [
        t
        for t in all_tickets
        if t.assigned_to == current_user.id
        and (not status_filter or t.status in status_filter)
        and (not type_filter or t.request_type in type_filter)
    ]

    # Filter unassigned tickets
    unassigned_tickets = [
        t
        for t in all_tickets
        if t.status == "Open"
        and t.assigned_to is None
        and (not type_filter or t.request_type in type_filter)
    ]

    # Retrieve admin feedback score average
    scores = [
        int(t.feedback) for t in assigned_tickets if t.feedback is not None
    ]
    average_score = sum(scores) / len(scores) if scores else 0

    return render_template(
        "admin/dashboard.html",
        user=current_user,
        assigned_tickets=assigned_tickets,
        unassigned_tickets=unassigned_tickets,
        average_score=average_score,
        status_options=STATUSES,
        request_type_options=REQUEST_TYPES,
    )


@bp.route("/manage-tickets", methods=["GET", "POST"])
@login_required
def manage_tickets():
    """
    Admin page to read, update and delete tickets.
    """
    from app import db
    from app.models import Ticket, User

    # Get filters
    status_filter = request.args.getlist("status")
    type_filter = request.args.getlist("request_type")
    assigned_to_filter = request.args.get("assigned_to")
    creator_user_filter = request.args.get("creator_user")

    # Retrieve all tickets and apply filters
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
            or (
                t.creator_user
                and str(t.creator_user.id) == creator_user_filter
            )
        )
    ]

    # Handle ticket deletion
    if "delete_ticket" in request.form:
        ticket_id = request.form.get("delete_ticket_id")
        delete_ticket = Ticket.query.get(ticket_id)

        db.session.delete(delete_ticket)
        db.session.commit()

        flash("Ticket deleted successfully.", "success")
        return redirect(url_for("admin.manage_tickets"))

    # Populate ticket update form
    admins = User.query.filter_by(role="Admin").all()
    all_admins = [
        (admin.id, f"{admin.firstname} {admin.surname}") for admin in admins
    ]
    creators = User.query.filter(
        User.id.in_(
            [
                t.creator_user.id
                for t in all_tickets
                if t.creator_user is not None
            ]
        )
    ).all()
    all_creators = [
        (creator.id, f"{creator.firstname} {creator.surname}")
        for creator in creators
    ]

    form = UpdateTicketForm()
    form.assigned_to.choices = [("", "Select an admin")] + all_admins
    show_edit_popup = False

    # Handle ticket update
    if form.validate_on_submit():
        ticket_id = form.id.data
        update_ticket = Ticket.query.get(ticket_id)

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
        user=current_user,
        all_tickets=filtered_tickets,
        show_edit_popup=show_edit_popup,
        status_options=STATUSES,
        request_type_options=REQUEST_TYPES,
        all_admins=all_admins,
        all_creators=all_creators,
    )


@bp.route("/manage-users", methods=["GET", "POST"])
@login_required
def manage_users():
    """
    Admin page to read and update users.
    """
    from app import db
    from app.models import User

    role_filter = request.args.get("role")

    # Retrieve all users and apply filters
    all_users = User.query.all()
    filtered_users = [
        u for u in all_users if (not role_filter or u.role == role_filter)
    ]

    # Handle user deletion
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

    # Handle user update
    if form.validate_on_submit():
        user_id = form.id.data
        update_user = User.query.get(user_id)

        update_user.firstname = form.firstname.data
        update_user.surname = form.surname.data
        update_user.email = form.email.data
        update_user.role = form.role.data

        db.session.commit()

        flash("User details updated successfully.", "success")

    return render_template(
        "admin/manage_users.html",
        form=form,
        user=current_user,
        all_users=filtered_users,
        role_options=ROLES,
    )
