from cursus_app.db import db


class Lesson(db.Model):
    """Subclass of :class:`SQLAlchemy.Model`.

    Represents a database table `lesson`.
    """
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
    course = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )

    def __repr__(self):
        return f"<Lesson {self.title}, index {self.index}>"

    def save(
        self, title: str, content: str, course: int, index: int = 0
            ) -> None:
        """Adds data and commits to the database table `lesson`.

        :param title: :attr: of :class:`Lesson`
        representing title
        :type title: str

        :param content: :attr: of :class:`Lesson`
        representing content
        :type content: str

        :param course: :attr: of :class:`Lesson`
        representing :class:`Course.id` to which `Lesson()`
        belongs to
        :type course: int

        :param index: :attr: of :class:`Lesson`
        representing sequence number of lessons  within one
        `Lesson.course`
        :type index: int

        :raises no exceptions:

        :returns: None
        :rtype: None
        """
        self.title = title
        self.content = content
        self.course = course

        db.session.add(self)
        db.session.commit()
        self.set_index(index)

    def update(self) -> None:
        """Updates data and commits to the database table `lesson`.

        :returns: None
        :rtype: None
        """
        db.session.add(self)
        db.session.commit()

    def get_all_lessons(self) -> list:
        """Gets list of lessons from db sorted by
        `Lesson.index` in the ascending order within
        one course `self.course`

        :returns: list of `Lesson` instances
        :rtype: list
        """
        lessons = Lesson.query.filter(
            Lesson.course == self.course
            ).order_by(Lesson.index.asc()).all()
        return lessons

    def _reindex_lessons(self, lessons: list, index: int) -> None:
        """Assigns new `index` value to `self` and rewrites
        other `lessons` indexes accordingly.

        :param lessons:
        representing list of `Lesson` instances sorted by
        `Lesson.index` in the ascending order
        :type lessons: list

        :param index:
        representing new `index` value to be
        assigned to `self.index`.
        :type index: int

        :raises IndexError: when pop() raises IndexError

        :returns: None
        :rtype: None
        """
        try:
            mover = lessons.pop(self.index - 1)
            lessons.insert(index - 1, mover)
        except IndexError as e:
            raise IndexError(e)
        for idx, lesson in enumerate(lessons, start=1):
            lesson.index = idx

    def set_index(self, index: int) -> None:
        """Sets new `index` value to `self.index` and commits
        changes to database table `lesson`. Rewrites
        other `lessons` indexes accordingly.
        If one of the cases below has been occurred
            `index == 0` or `index > number of existing lessons`
            or `self.index is None`
        then the last index value to be assigned to `self.index`

        :param index:
        representing new `index` value to be set as `self.index`
        and saved to db.
        :type index: int

        :raises ValueError: if `index` < 0

        :returns: None
        :rtype: None
        """
        if index < 0:
            raise ValueError("Index should be positive number (>0)")
        existing_lessons = self.get_all_lessons()
        if existing_lessons:
            if not self.index:
                self.index = len(existing_lessons)
                db.session.commit()
                return None
            if index >= len(existing_lessons) or index == 0:
                index = len(existing_lessons)
            self._reindex_lessons(existing_lessons, index)
            db.session.commit()
            return None
