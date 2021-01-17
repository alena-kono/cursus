from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class NewCourseForm(FlaskForm):
    """Subclass of :class: `flask_wtf.Flask-Form`.
    Represents form for adding a new `Course`

    :attr title: StringField

    :attr description: TextAreaField

    :attr submit: SubmitField
    """
    title = StringField(
        label="Title",
        validators=[
            DataRequired(),
            Length(max=32, message="Title should be 32 characters max")
            ],
        render_kw={"class": "form-control", "placeholder": "Title"}
        )
    description = TextAreaField(
        label="Description",
        validators=[
            DataRequired(),
            Length(max=255, message="Description should be 255 characters max")
            ],
        render_kw={
            "class": "form-control",
            "placeholder": "Description", "rows": 5}
        )
    submit = SubmitField(
        label="Create",
        render_kw={"class": "btn btn-primary btn-lg mb-4 w-100"}
        )

    def validate_title_chars(self, title: str) -> ValidationError:
        """Validates `title` by checking whether all characters
        except the whitespace is alphanumeric (letters(a-z) and/or digits(0-9))

        :param title: field of :class:`NewCourseForm` to be validated
        :type title: str

        :raises ValidationError: if `title` contains
        non-alphanumeric characters

        :returns: None
        :rtype: None
        """
        title = title.replace(" ", "")
        if not title.isalnum():
            msg = "Title should contain only letters(a-z) and/or digits(0-9)"
            raise ValidationError(msg)
