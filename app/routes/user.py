"""
User routes for the application.
"""

from datetime import datetime

from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from app.forms.feedback import FeedbackForm
from app.forms.ticket import CreateTicketForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """
    User dashboard displaying all tickets created by the user.
    """
    from app.models import Ticket

    feedback_form = FeedbackForm()

    # Retrieve tickets for the user
    all_tickets = Ticket.query.filter_by(creator=current_user.id).all()

    # Retrieve tickets by status for dashboard summary
    open_tickets = [t for t in all_tickets if t.status == "Open"]
    in_progress_tickets = [t for t in all_tickets if t.status == "In Progress"]
    on_hold_tickets = [t for t in all_tickets if t.status == "On Hold"]
    resolved_tickets = [t for t in all_tickets if t.status == "Resolved"]
    closed_tickets = [t for t in all_tickets if t.status == "Closed"]

    return render_template(
        "user/dashboard.html",
        feedback_form=feedback_form,
        user=current_user,
        all_tickets=all_tickets,
        open_tickets=open_tickets,
        in_progress_tickets=in_progress_tickets,
        on_hold_tickets=on_hold_tickets,
        resolved_tickets=resolved_tickets,
        closed_tickets=closed_tickets,
    )


@bp.route("/create-ticket", methods=["GET", "POST"])
@login_required
def create_ticket():
    """
    Create a new ticket.
    """
    from app import db
    from app.models import Ticket

    form = CreateTicketForm()

    if form.validate_on_submit():

        # Create new ticket
        new_ticket = Ticket(
            request_type=form.request_type.data,
            date_opened=datetime.now().date(),
            title=form.title.data,
            description=form.description.data,
            status="Open",
            creator=current_user.id,
        )

        # Save new ticket to database
        db.session.add(new_ticket)
        db.session.commit()

        flash("Ticket created successfully!", "success")

    return render_template(
        "user/create_ticket.html", form=form, user=current_user
    )


@bp.route("/update-ticket", methods=["GET", "POST"])
@login_required
def update_ticket():
    """
    Update an existing ticket.
    """
    from app import db
    from app.models import Ticket

    form = CreateTicketForm()

    # Retrieve tickets for the user
    all_tickets = Ticket.query.filter_by(
        creator=current_user.id, status="Open"
    ).all()

    if form.validate_on_submit():
        # Retrieve ticket from the database
        ticket_id = request.form.get("ticket_id")
        ticket = Ticket.query.get_or_404(ticket_id)

        # Update ticket details
        ticket.request_type = form.request_type.data
        ticket.title = form.title.data
        ticket.description = form.description.data

        # Save changes to database
        db.session.commit()
        flash("Ticket updated successfully!", "success")

    return render_template(
        "user/update_ticket.html",
        form=form,
        user=current_user,
        all_tickets=all_tickets,
    )


@bp.route("/submit-feedback", methods=["POST"])
@login_required
def submit_feedback():
    """
    Submit feedback for a ticket.
    """
    from app import db
    from app.models import Ticket

    form = FeedbackForm()

    # Retrieve tickets for the user
    all_tickets = Ticket.query.filter_by(creator=current_user.id).all()

    if form.validate_on_submit():
        ticket_id = form.id.data
        rating = form.rating.data

        # Retrieve the ticket from the database
        ticket = Ticket.query.get(ticket_id)

        if ticket:
            # Save feedback to the database
            ticket.feedback = rating
            ticket.status = "Closed"
            db.session.commit()
            flash("Thank you for your feedback!", "success")
        else:
            flash("Error submitting feedback. Ticket not found.", "danger")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f"Error in {getattr(form, field).label.text}: {error}",
                    "danger",
                )

    return render_template(
        "user/dashboard.html",
        user=current_user,
        feedback_form=form,
        all_tickets=all_tickets,
    )
