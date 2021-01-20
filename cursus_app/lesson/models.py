from cursus_app.db import db


class Lesson(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
        )
    title = db.Column(
        db.String(32), index=True, nullable=False
        )
    content = db.Column(
        db.String(), nullable=False
        )
    index = db.Column(
        db.Integer, nullable=False
        )
    course = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )

    def __repr__(self):
        return f"<Lesson {self.title}>"

    def save(self, title: str, content: str, index: int, course: int) -> None:
        """Adds data and commits to the database table `lesson`.

        :param username: :attr: of :class:`Lesson`
        representing username
        :type username: str

        :param password: :attr: of :class:`Lesson`
        representing user password
        :type title: str

        :raises no exceptions:

        :returns: None
        :rtype: None
        """
        self.title = title
        self.content = content
        self.index = index
        self.course = course
        db.session.add(self)
        db.session.commit()
