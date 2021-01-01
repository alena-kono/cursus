from cursus_app.db import db


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
