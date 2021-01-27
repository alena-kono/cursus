from typing import List, Tuple

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
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
    topics = StringField(
        label="topics",
        render_kw={
            "class": "form-control",
            "placeholder": "Indicate topics separated by space"
            }
        )
    submit = SubmitField(
        label="Create course and save it to a draft",
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


class FilterByTutorAndTopicForm(FlaskForm):
    """Subclass of :class: `flask_wtf.Flask-Form`.
    Represents form for filtering courses by two fields:
    `tutors` and `topics`.

    :attr filter_by_tutor: SelectField with integer values

    :attr filter_by_topic: SelectField with integer values

    :attr submit: SubmitField
    Represents 'Show' submit button when filtering courses
    """
    filter_by_tutor = SelectField(
        label="Filter by tutor",
        coerce=int
        )
    filter_by_topic = SelectField(
        label="Filter by topic",
        coerce=int
        )
    submit = SubmitField(
        label="Show",
        render_kw={"class": "btn btn-primary btn-sm"}
    )

    @staticmethod
    def _get_all_tutor_choices(tutors: list) -> List[Tuple]:
        """Repacks list with `User()` instances - `tutors` -
        into list of tuples (`tutor.id`, `tutor.username`).

        :param tutors: unique list of Users that are tutors
        :type: list
        :return: list of tuple pairs (tutor.id, tutor.username)
        :rtype: List[Tuple]
        """
        choices = [(0, "all")]
        for tutor in tutors:
            choices.append((tutor.id, tutor.username))
        return choices

    @staticmethod
    def _get_all_topic_choices(topics: list) -> List[Tuple]:
        """Repacks list with `Topic()` instances - `topics` -
        into list of tuples (`topic.id`, `topic.name`).

        :param topics: unique list of Topics
        :type: list
        :return: list of tuple pairs (topic.id, topic.name)
        :rtype: List[Tuple]
        """
        choices = [(0, "all")]
        for topic in topics:
            choices.append((topic.id, topic.name))
        return choices

    def load_choices(self, tutors: list, topics: list) -> None:
        """Loads choices for two fields in a `FilterByTutorAndTopicForm`.

        :param tutors: list of tuples (`tutor.id`, `tutor.username`)
        :type: List[Tuple]

        :param topics: list of tuples (`topic.id`, `topic.name`)
        :type: List[Tuple]

        :return: None
        :rtype: None
        """
        self.filter_by_tutor.choices = self._get_all_tutor_choices(tutors)
        self.filter_by_topic.choices = self._get_all_topic_choices(topics)
