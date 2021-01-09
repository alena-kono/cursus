from datetime import datetime
from random import choice, randint

from cursus_app import db
from cursus_app.course.models import Course, Topic
from cursus_app.lesson.models import Lesson
from cursus_app.user.models import User


def create_users() -> list:
    USERS = ["creator", "musician", "artist"]
    created = []
    for user in USERS:
        new_user = User(username=user)
        new_user.set_password(password="pass")
        created.append(new_user)
    return created


def create_courses(authors_number: int = 3) -> list:
    COURSES_PUBLISHED_AT = {
        "Maths": datetime(2015, 4, 28),
        "Advanced Guitar": datetime(2018, 7, 11),
        "English": datetime.now(),
        "Chemistry": datetime.now(),
        "Ukulele Basics": datetime.now(),
        }
    DEFAULT_DESC = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    created = []
    for title, date in COURSES_PUBLISHED_AT.items():
        new_course = Course(
            title=title,
            description=DEFAULT_DESC,
            published_at=date,
            author=randint(1, authors_number)
        )
        created.append(new_course)
    return created


def create_lessons(courses_number: int = 5) -> list:
    LESSONS = ["Basics", "Basics II", "Intermediate", "Advanced"]
    DEFAULT_CONTENT = "Lorem ipsum dolor sit amet, consectetur adipiscing\
        elit, sed do eiusmod tempor incididunt ut labore et dolore magna\
        aliqua.Ut enim ad minim veniam, quis nostrud exercitation\
        ullamco laboris nisi ut aliquip ex ea commodo consequat."
    created = []
    for lesson in LESSONS:
        new_lesson = Lesson(
            title=lesson,
            content=DEFAULT_CONTENT,
            index=randint(1, 10),
            course=randint(1, courses_number)
            )
        created.append(new_lesson)
    return created


def create_topics(courses: list) -> list:
    TOPICS = ["music", "science", "random"]
    created = []
    for topic in TOPICS:
        new_topic = Topic(name=topic)
        new_topic.courses.append(choice(courses))
        created.append(new_topic)
    return created


def populate_db_with_test_data():
    """Populate database tables with test data"""
    users = create_users()
    courses = create_courses(authors_number=len(users))
    lessons = create_lessons(courses_number=len(courses))
    topics = create_topics(courses=courses)
    records = [users, courses, lessons, topics]
    for record in records:
        for obj in record:
            db.session.add(obj)
    db.session.commit()


def setup_demo_db():
    """Create db tables and populate them with test data for demo.
    Run once before the first request to this instance
    of the application.
    """
    db.drop_all()
    db.create_all()
    populate_db_with_test_data()
