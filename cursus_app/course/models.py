from datetime import datetime

from cursus_app.db import db
from cursus_app.lesson.models import Lesson
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
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now()
        )
    published_at = db.Column(
        db.DateTime, nullable=True
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
            self, title: str, description: str, author: int, topics: str = ""
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

        :param topics: represents related topics
        :type topics: str

        :raises no exceptions:

        :returns: None
        :rtype: None
        """
        self.title = title
        self.description = description
        self.author = author
        if topics:
            self.parse_topics(topics)
        db.session.add(self)
        db.session.commit()

    def parse_topics(self, topics: str) -> None:
        topics = topics.split()
        for topic in topics:
            existing_topic = Topic.query.filter(Topic.name == topic).first()
            if existing_topic:
                self.topics.append(existing_topic)
            else:
                self.topics.append(Topic(name=topic))

    def publish(self):
        self.is_published = True
        self.published_at = datetime.now()
        db.session.commit()

    @staticmethod
    def get_all_published_courses() -> list:
        courses = Course.query.filter(
            Course.is_published.is_(True)
        ).order_by(Course.published_at.desc()).all()
        return courses

    def get_author_username(self):
        return User.query.get(self.author).username

    @staticmethod
    def get_tutors():
        tutors = Course.query.group_by(Course.author)
        return tutors

    @staticmethod
    def get_courses_by_tutor(tutor_id: int) -> list:
        courses_by_tutor = Course.query.filter(
            Course.author == tutor_id).order_by(
                Course.published_at.desc()).all()
        return courses_by_tutor

    def get_all_lessons(self) -> list:
        lessons = db.session.query(Lesson).filter(
            Course.id == Lesson.course
        ).filter(
            Course.id == self.id
        ).order_by(Lesson.index.asc()).all()
        return lessons

    def get_all_topics(self) -> list:
        all_topics = self.topics
        return all_topics

    @staticmethod
    def filter_by_tutor_and_topic(tutor_id: int, topic_id: int) -> list:
        courses = Course.query.filter(
            Course.topics.any(Topic.id == topic_id),
            Course.author == tutor_id
        ).order_by(Course.published_at.desc()).all()
        return courses


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

    def get_all_courses(self) -> list:
        courses_by_topic = Course.query.filter(
            Course.topics.any(Topic.id == self.id)
            ).all()
        return courses_by_topic
