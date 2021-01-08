from cursus_app.db import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    ROLES = ('admin', 'tutor', 'student')

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

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def save(
        self, username: str, password: str, role: str = "student"
            ) -> None:
        self.username = username
        self.set_password(password)
        self.role = role
        db.session.add(self)
        db.session.commit()
