from flask_wtf import FlaskForm
from markdown import markdown
from markdown_checklist.extension import ChecklistExtension
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class NewLessonForm(FlaskForm):
    """Subclass of :class: `flask_wtf.Flask-Form`.
    Represents form for adding a new `Lesson`

    :attr title: StringField

    :attr content: TextAreaField

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
    content = TextAreaField(
        label="Description",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "Content", "rows": 20}
        )
    submit = SubmitField(
        label="Create",
        render_kw={"class": "btn btn-primary btn-lg mb-4 w-100"}
        )

    def convert_to_html(self) -> str:
        """Convert a markdown `self.content.data` to HTML and return
        HTML as a unicode string.

        :raises: no exceptions

        :returns: HTML as unicode string
        :rtype: str
        """
        if self.content.data:
            html_content = markdown(
                self.content.data,
                extensions=[ChecklistExtension()]
                )
            return html_content
        return None

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
