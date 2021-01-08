from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NewCourse(FlaskForm):
    title = StringField(
        label="Title",
        validators=[DataRequired(), Length(max=10)],
        render_kw={"class": "form-control", "placeholder": "Title"}
        )
    description = TextAreaField(
        label="Description",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "Description", "rows": 5}
        )
    submit = SubmitField(
        label="Create",
        render_kw={"class": "btn btn-primary btn-lg mb-4 w-100"}
        )
