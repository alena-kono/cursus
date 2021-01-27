from cursus_app import db
from cursus_app.course.models import Course, Topic
from cursus_app.lesson.models import Lesson
from cursus_app.user.models import User
from factory import Faker, Sequence, alchemy, post_generation
from werkzeug.security import generate_password_hash


class RandomUserFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = Sequence(lambda n: n + 1)
    username = Faker("last_name")
    password = generate_password_hash("pass")


class RandomTopicFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Topic
        sqlalchemy_session = db.session

    id = Sequence(lambda n: n + 1)
    name = Faker("word")


class RandomCourseFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Course
        sqlalchemy_session = db.session

    id = Sequence(lambda n: n + 1)
    title = Faker("word")
    description = Faker("paragraph", locale="en_US")
    created_at = Faker("date_time")
    published_at = Faker("date_time")
    is_active = True
    is_published = True
    tutor = 1

    @post_generation
    def topics(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for topic in extracted:
                self.topics.append(topic)


class RandomLessonFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Lesson
        sqlalchemy_session = db.session
    id = Sequence(lambda n: n + 1)
    title = Faker("word")
    content = Faker("paragraph", locale="en_US")
    course = 1
    index = 1

    @staticmethod
    def create_for_each_course(courses_num: int, lessons_per_course_num: int):
        for course in range(1, courses_num + 1):
            for lesson in range(1, lessons_per_course_num + 1):
                RandomLessonFactory.create(
                    course=course,
                    index=lesson
                    )
