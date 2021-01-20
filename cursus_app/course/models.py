from datetime import datetime

from cursus_app.db import db
from cursus_app.user.models import User

topics = db.Table(
    "topics",
    db.Column(
        "topic_id", db.Integer, db.ForeignKey("topic.id"), primary_key=True),
    db.Column(
        "course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True)
)


class Course(db.Model):
    """Subclass of :class:`SQLAlchemy.Model`.

    Represents a database table `course`.
    """
    id = db.Column(
        db.Integer, primary_key=True
    )
    title = db.Column(
        db.String(32), index=True, nullable=False
        )
    description = db.Column(
        db.String(), nullable=False
        )
    published_at = db.Column(
        db.Date, nullable=False, default=datetime.now()
        )
    is_active = db.Column(
        db.Boolean, nullable=False, default=True
    )
    is_published = db.Column(
        db.Boolean, nullable=False, default=False
    )
    author = db.Column(
        db.Integer, db.ForeignKey("user.id")
        )
    student = db.Column(
        db.Integer, db.ForeignKey("user.id")
        )
    course_author = db.relationship(
        "User", foreign_keys=[author]
        )
    course_student = db.relationship(
        "User", foreign_keys=[student]
        )
    topics = db.relationship(
        "Topic", secondary=topics, lazy="subquery",
        backref=db.backref("courses", lazy=True)
        )

    def __repr__(self):
        return f"<Course {self.title}>"

    def save(
            self, title: str, description: str, author: int
    ) -> None:
        """Adds data and commits to the database table `course`.

        :param title: :attr: of :class:`Course`
        representing course title
        :type title: str

        :param description: :attr: of :class:`Course`
        representing course description
        :type description: str

        :param author: :attr: of :class:`Course`
        representing id of the course author (instance of :class:`User`)
        :type author: int

        :raises no exceptions:

        :returns: None
        :rtype: None
        """
        self.title = title
        self.description = description
        self.author = author
        db.session.add(self)
        db.session.commit()

    def get_author_username(self):
        # remove when moving db queries to separate utils.py file
        return User.query.get(self.author).username

    @staticmethod
    def get_courses_by_tutor(tutor_id: int):
        courses_by_tutor = Course.query.filter(
            Course.author == tutor_id).order_by(
                Course.published_at.desc()).all()
        return courses_by_tutor


class Topic(db.Model):
    """Subclass of :class:`SQLAlchemy.Model`.

    Represents a database table `topic`.
    """
    id = db.Column(
        db.Integer, primary_key=True
        )
    name = db.Column(
        db.String(32), unique=True, index=True, nullable=False
        )

    def __repr__(self):
        return f"<Topic {self.name}>"
