from cursus_app.auth.forms import LoginForm
from cursus_app.user.models import User
from cursus_app.auth.utils import get_auth_navbar_btn
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    page_title = "Cursus - Login"
    login_form = LoginForm()
    auth_btns = get_auth_navbar_btn()
    return render_template(
        "auth/login.html",
        page_title=page_title,
        form=login_form,
        auth_btns=auth_btns
    )


@auth_blueprint.route("/process-login/", methods=["POST"])
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
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/logout/")
def logout():
    logout_user()
    flash("Successful logout")
    return redirect(url_for("home.index"))
