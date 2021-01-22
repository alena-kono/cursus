from cursus_app.db import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    """Subclass of :class:`SQLAlchemy.Model`
    and :class:`flask_login.UserMixin`

    Represents a database table `user`.
    """
    id = db.Column(
        db.Integer, primary_key=True
    )
    username = db.Column(
        db.String(32), unique=True, index=True, nullable=False
        )
    password = db.Column(
        db.String(128), nullable=False
        )
    userpic_url = db.Column(
        db.String(), nullable=True
        )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:
        """Hashes `password` and sets it as :attr:`User.password`.

        :param password: :attr: of :class:`User`
        representing user password
        :type password: str

        :raises no exceptions:

        :returns: None
        :rtype: None
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks a `password` against a given salted and hashed `password`.

        :param password: :attr: of :class:`User`
        representing user password
        :type password: str

        :raises no exceptions:

        :returns: True or False
        :rtype: bool
        """
        return check_password_hash(self.password, password)

    def save(self, username: str, password: str) -> None:
        """Adds data and commits to the database table `user`.

        :param username: :attr: of :class:`User`
        representing username
        :type username: str

        :param password: :attr: of :class:`User`
        representing user password
        :type title: str

        :raises no exceptions:

        :returns: None
        :rtype: None
        """
        self.username = username
        self.set_password(password)
        db.session.add(self)
        db.session.commit()
