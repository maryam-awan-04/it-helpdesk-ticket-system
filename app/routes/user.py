"""
User routes for the application
"""

from flask import Blueprint, redirect, render_template, request, url_for

from app.forms.feedback import FeedbackForm
from app.forms.ticket import Ticket

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    feedback_form = FeedbackForm()

    return render_template("user/dashboard.html", feedback_form=feedback_form)


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
