"""
User routes for the application
"""

from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from app.forms.feedback import FeedbackForm
from app.forms.ticket import TicketForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    from app.models import Ticket, User

    feedback_form = FeedbackForm()

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    # Retrieve tickets for the user
    all_tickets = Ticket.query.filter_by(creator=user.id).all()

    # Retrieve tickets by status for dashboard summary
    open_tickets = [t for t in all_tickets if t.status == "Open"]
    in_progress_tickets = [t for t in all_tickets if t.status == "In Progress"]
    on_hold_tickets = [t for t in all_tickets if t.status == "On Hold"]
    resolved_tickets = [t for t in all_tickets if t.status == "Resolved"]
    closed_tickets = [t for t in all_tickets if t.status == "Closed"]

    return render_template(
        "user/dashboard.html",
        feedback_form=feedback_form,
        user=user,
        all_tickets=all_tickets,
        open_tickets=open_tickets,
        in_progress_tickets=in_progress_tickets,
        on_hold_tickets=on_hold_tickets,
        resolved_tickets=resolved_tickets,
        closed_tickets=closed_tickets,
    )


@bp.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():
    from app import db
    from app.models import Ticket, User

    form = TicketForm()

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    if form.validate_on_submit():

        # Create new ticket
        new_ticket = Ticket(
            request_type=form.request_type.data,
            date_opened=datetime.now().date(),
            title=form.title.data,
            description=form.description.data,
            status="Open",
            creator=user.id,
        )

        # Save new ticket to database
        db.session.add(new_ticket)
        db.session.commit()

        flash("Ticket created successfully!", "success")

    return render_template("user/create_ticket.html", form=form, user=user)


@bp.route("/update-ticket", methods=["GET", "POST"])
def update_ticket():
    from app import db
    from app.models import Ticket, User

    form = TicketForm()

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    # Retrieve tickets for the user
    all_tickets = Ticket.query.filter_by(creator=user.id, status="Open").all()

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
        "user/update_ticket.html", form=form, user=user, all_tickets=all_tickets
    )


from flask import jsonify


@bp.route("/submit-feedback", methods=["GET", "POST"])
def submit_feedback():

    form = FeedbackForm()

    if form.validate_on_submit():
        ticket_id = request.form.get("ticket_id")

        # retrieve the ticket from db
        ticket = ticket_id

        if not ticket:
            return jsonify({"success": False, "error": "Ticket not found"}), 404

        # save feedback to db

        return jsonify({"success": True, "message": "Thank you for your feedback!"})
    else:
        return jsonify({"success": False, "errors": form.errors}), 400
