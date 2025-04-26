"""
Authentication routes for the application
e.g. login, registration, logout
"""

from flask import Blueprint, flash, redirect, render_template, url_for

from app.forms import LoginForm, RegistrationForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Authentication logic
        flash("Login successful", "success")
        return redirect(url_for(""))  # add redirect URL
    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    from app import bcrypt, db
    from app.models import User

    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered. Please sign in.", "error")
            return redirect(url_for("auth.register"))

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
