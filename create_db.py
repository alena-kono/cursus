from factory import fuzzy, random

from cursus_app import config, create_app, db
from factories.models import (RandomCourseFactory, RandomLessonFactory,
                              RandomTopicFactory, RandomUserFactory)


def create_db_tables():
    db.drop_all()
    db.create_all()


def populate_db_with_demo_data(
    users_num: int = 10,
    courses_num: int = 10,
    lessons_per_course_num: int = 5
        ) -> None:
    random.reseed_random("cursus_app")
    random.get_random_state()

    RandomUserFactory.create(username="creator")
    RandomUserFactory.create_batch(size=users_num)
    topic = RandomTopicFactory.create_batch(size=2)
    topics = RandomTopicFactory.create_batch(size=2)
    RandomCourseFactory.create_batch(
        size=courses_num,
        tutor=fuzzy.FuzzyChoice(range(1, users_num + 1)),
        topics=fuzzy.FuzzyChoice([topic, topics])
        )
    RandomLessonFactory.create_for_each_course(
        courses_num=courses_num,
        lessons_per_course_num=lessons_per_course_num)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        if config.DEMO_DB:
            create_db_tables()
            populate_db_with_demo_data(
                courses_num=20,
                lessons_per_course_num=10
            )
        else:
            create_db_tables()
