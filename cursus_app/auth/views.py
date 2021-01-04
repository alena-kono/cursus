from cursus_app.auth.forms import LoginForm
from cursus_app.user.models import User
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    page_title = "Cursus - Login"
    login_form = LoginForm()
    return render_template(
        "auth/login.html",
        page_title=page_title,
        form=login_form
    )


@login_blueprint.route("/process-login/", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            User.username == form.username.data
            ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Successful login")
            return redirect(url_for("home.index"))
    flash("Incorrect username or password")
    return redirect(url_for("login.login"))


@login_blueprint.route("/logout/")
def logout():
    logout_user()
    flash("Successful logout")
    return redirect(url_for("home.index"))
