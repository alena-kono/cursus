from cursus_app.db import db


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
