from cursus_app.db import db

topics = db.Table(
    "topics",
    db.Column(
        "topic_id", db.Integer, db.ForeignKey("topic.id"), primary_key=True),
    db.Column(
        "course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True)
)


class Course(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )
    title = db.Column(
        db.String(32), index=True, nullable=False
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
