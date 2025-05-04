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
    from app.models import User

    feedback_form = FeedbackForm()

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    return render_template(
        "user/dashboard.html", feedback_form=feedback_form, user=user
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
            date_opened=datetime.now(),
            title=form.title.data,
            description=form.description.data,
            status="open",
            creator=user.id,
        )

        # Save new ticket to database
        db.session.add(new_ticket)
        db.session.commit()

        flash("Ticket created successfully!", "success")

    return render_template("user/create_ticket.html", form=form, user=user)


@bp.route("/update-ticket", methods=["GET", "POST"])
def update_ticket():
    from app.models import User

    form = TicketForm()

    user_email = session.get("user_email")
    user = User.query.filter_by(email=user_email).first()

    if form.validate_on_submit():
        return redirect(url_for("user.dashboard"))

    return render_template("user/update_ticket.html", form=form, user=user)


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
