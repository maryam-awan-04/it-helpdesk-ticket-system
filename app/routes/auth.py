"""
Authentication routes for the application
e.g. login, registration, logout
"""

from flask import Blueprint, flash, redirect, render_template, url_for

from app.forms.login import LoginForm
from app.forms.registration import RegistrationForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Direct user to dashboard according to role
        if form.user.role == "Admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("user.dashboard"))

    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    from app import bcrypt, db
    from app.models import User

    form = RegistrationForm()

    if form.validate_on_submit():
        # Create new user with hashed password
        input_password = form.password.data
        hashed = bcrypt.generate_password_hash(input_password).decode("utf-8")
        new_user = User(
            firstname=form.firstname.data,
            surname=form.surname.data,
            email=form.email.data,
            password=hashed,
            role=form.role.data,
        )

        # Save new user to database
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please sign in.", "success")

    return render_template("auth/register.html", form=form)


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    from flask import session

    # Clear the session
    session.clear()

    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
