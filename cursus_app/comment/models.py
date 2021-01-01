from cursus_app.db import db


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
