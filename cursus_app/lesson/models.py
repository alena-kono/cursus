from cursus_app.db import db
from cursus_app.course.models import Course


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
        db.Integer, nullable=True
        )
    next_lesson_index = db.Column(
        db.Integer, nullable=True
        )
    course = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )

    def __repr__(self):
        return f"<Lesson {self.title}>"

    def get_last_index(self) -> int:
        last_les = Lesson.query.filter(
            Course.id == self.course
            ).order_by(Lesson.index.desc()).first()
        if not last_les:
            return 0
        return last_les.index

    def save(
        self,
        title: str, content: str, course: int, index: int = 0
            ) -> None:
        """Adds data and commits to the database table `lesson`.

        :param title: :attr: of :class:`Lesson`
        representing title
        :type title: str

        :param content: :attr: of :class:`Lesson`
        representing content
        :type content: str

        :param course: :attr: of :class:`Lesson`
        representing :class:`Course.id` to which `Lesson()` belongs to
        :type course: int

        :param index: :attr: of :class:`Lesson`
        representing index (ie serial number of each `Lesson()`
        in a course with id=`self.course`)
        :type index: int, default=0

        :raises no exceptions:

        :returns: None
        :rtype: None
        """
        self.title = title
        self.content = content
        self.course = course
        if not index:
            self.index = self.get_last_index() + 1

        db.session.add(self)
        db.session.commit()
