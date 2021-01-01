from cursus_app.db import db


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
