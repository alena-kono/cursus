from cursus_app.user.models import User
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class LoginForm(FlaskForm):
    """Subclass of :class: `flask_wtf.Flask-Form`. Represents login form.

    :attr username: StringField

    :attr password: PasswordField

    :attr submit: SubmitField

    :attr remember_me: BooleanField
    """
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
    """Subclass of :class: `flask_wtf.Flask-Form`. Represents sign up form.

    :attr username: StringField

    :attr password_1: PasswordField

    :attr password_2: PasswordField that validates
    equality to `password_1` field

    :attr submit: SubmitField
    """
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
        validators=[
            DataRequired(),
            EqualTo("password_1", "Passwords do not match. Please try again.")
            ],
        render_kw={"class": "form-control", "placeholder": "Password"}
        )
    submit = SubmitField(
        label="Sign Up",
        render_kw={"class": "btn btn-primary btn-lg mb-4 w-100"}
        )

    def validate_username(self, username: str) -> ValidationError:
        """Validates username by checking whether instance of
        :class: `User` with `username` is already presented in the database.

        :param username: field of :class:`SignupForm` to be validated
        :type username: str

        :raises ValidationError: if `username` is presented in the
        database

        :returns: None
        :rtype: None
        """
        user = User.query.filter(
            User.username == username.data
            ).first()
        if user:
            raise ValidationError(
                f"User with username '{username.data}' already exists"
            )
