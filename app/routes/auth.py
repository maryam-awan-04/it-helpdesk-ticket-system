"""
Authentication routes for the application,
including login, registration, and logout.
"""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from app.forms.login import LoginForm
from app.forms.registration import RegistrationForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    Redirects to the appropriate dashboard based on user role.
    """
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user)
        flash("Login successful!", "info")

        # Redirect based on role
        if form.user.role == "Admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("user.dashboard"))

    # Render the login form for GET requests
    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration.
    Creates a new user using details from the form
    then saves it to the database.
    """
    from app import bcrypt, db
    from app.models import User

    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the password
        input_password = form.password.data
        hashed = bcrypt.generate_password_hash(input_password).decode("utf-8")

        # Create new user
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
    """
    Handles user logout.
    Logs out the user and redirects to the login page.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
