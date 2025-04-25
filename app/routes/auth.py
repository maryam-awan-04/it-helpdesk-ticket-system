from flask import Blueprint, flash, redirect, render_template, url_for

from app.forms.login import LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Authentication logic
        flash("Login successful", "success")
        return redirect(url_for(""))  # add redirect URL
    return render_template("auth/login.html", form=form)


@bp.route("/register")
def register():
    # Registration logic
    return render_template("auth/register.html")
