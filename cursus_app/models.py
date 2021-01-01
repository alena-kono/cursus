from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

topics = db.Table(
    "topics",
    db.Column(
        "topic_id", db.Integer, db.ForeignKey("topic.id"), primary_key=True),
    db.Column(
        "course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True)
)


class User(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )
    username = db.Column(
        db.String(32), unique=True, index=True, nullable=False
        )
    password = db.Column(
        db.String(128), nullable=False
        )
    role = db.Column(
        db.String(32), nullable=False
        )
    userpic_url = db.Column(
        db.String(), nullable=True
        )

    def __repr__(self):
        return f"<User {self.username}>"


class Course(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )
    title = db.Column(
        db.String(32), unique=True, index=True, nullable=False
        )
    description = db.Column(
        db.String(), nullable=True
        )
    start_date = db.Column(
        db.Date, nullable=True
        )
    end_date = db.Column(
        db.Date, nullable=True
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


class Topic(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
        )
    name = db.Column(
        db.String(32), unique=True, index=True, nullable=False
        )

    def __repr__(self):
        return f"<Topic {self.name}>"


class Lesson(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
        )
    title = db.Column(
        db.String(32), unique=True, index=True, nullable=False
        )
    description = db.Column(
        db.String(), nullable=True
        )
    course = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )

    def __repr__(self):
        return f"<Lesson {self.title}>"


class Comment(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
        )
    text = db.Column(
        db.String(), nullable=True
        )
    lesson = db.Column(
        db.Integer, db.ForeignKey("lesson.id")
    )
    published_at = db.Column(
        db.DateTime, nullable=True
        )

    def __repr__(self):
        return f"<Comment {self.title}>"


class Attachment(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
        )
    file_url = db.Column(
        db.String(), nullable=False
        )
    media_type = db.Column(
        db.String(32), nullable=False
        )
    lesson = db.Column(
        db.Integer, db.ForeignKey("lesson.id")
    )

    def __repr__(self):
        return f"<Attachment {self.title}>"
