from cursus_app.auth.forms import LoginForm, SignupForm
from cursus_app.user.models import User
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    page_title = "Cursus - Login"
    login_form = LoginForm()
    return render_template(
        "auth/login.html",
        page_title=page_title,
        form=login_form,
        current_user=current_user
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
            flash("Successful login", "success")
            return redirect(url_for("home.index"))
    flash("Incorrect username or password", "warning")
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/logout/")
def logout():
    logout_user()
    flash("Successful logout", "success")
    return redirect(url_for("home.index"))


@auth_blueprint.route("/signup/")
def signup():
    page_title = "Cursus - Sign Up"
    signup_form = SignupForm()
    return render_template(
        "auth/signup.html",
        page_title=page_title,
        form=signup_form,
        current_user=current_user
    )


@auth_blueprint.route("/process-signup/", methods=["POST"])
def process_signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter(
            User.username == form.username.data
            ).first()
        if user:
            flash(
                f"User with username '{form.username.data}' already exists",
                "warning"
                )
            return redirect(url_for("auth.signup"))
        if form.password_1.data == form.password_2.data:
            new_user = User()
            new_user.save(
                username=form.username.data,
                password=form.password_1.data
                )
            flash(
                "You've successfully signed up for Cursus!\nPlease log in.",
                "success"
                )
            return redirect(url_for("auth.login"))
    flash(
        "Passwords do not match. Please try again.",
        "warning"
        )
    return redirect(url_for("auth.signup"))
