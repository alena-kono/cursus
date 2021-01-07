from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Username"}
        )
    password = PasswordField(
        label="Password",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Password"}
        )
    submit = SubmitField(
        label="Log in",
        render_kw={"class": "btn btn-primary btn-lg mb-4 w-100"}
        )
    remember_me = BooleanField(
        label="Remember me",
        default=True,
        render_kw={"class": "btn btn-primary"}
        )


class SignupForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Username"}
        )
    password_1 = PasswordField(
        label="Password",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Password"}
        )
    password_2 = PasswordField(
        label="Confirm your password",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Password"}
        )
    submit = SubmitField(
        label="Sign Up",
        render_kw={"class": "btn btn-primary btn-lg mb-4 w-100"}
        )
