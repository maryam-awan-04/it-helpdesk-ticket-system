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
    form = RegistrationForm()
    if form.validate_on_submit():
        # Registration logic
        flash("Registration successful", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)
