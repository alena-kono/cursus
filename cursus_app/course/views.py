from cursus_app.auth.utils import get_auth_navbar_btn
from cursus_app.course.models import Course, Topic
from cursus_app.lesson.models import Lesson
from flask import Blueprint, render_template
from flask_login import login_required

course_blueprint = Blueprint("course", __name__, url_prefix="/courses")


@course_blueprint.route("/")
def index():
    page_title = "Cursus - all courses"
    auth_btns = get_auth_navbar_btn()
    courses = Course.query.all()
    return render_template(
        "course/courses.html",
        page_title=page_title,
        auth_btns=auth_btns,
        courses=courses
    )


@course_blueprint.route("/topics/")
def topics():
    page_title = "Cursus - all topics"
    auth_btns = get_auth_navbar_btn()
    topics = Topic.query.all()
    return render_template(
        "course/topics.html",
        page_title=page_title,
        auth_btns=auth_btns,
        topics=topics
    )


@course_blueprint.route("/topics/<topic_name>")
def courses_in_topic(topic_name):
    page_title = f"Cursus - {topic_name}"
    auth_btns = get_auth_navbar_btn()
    courses_in_topic = Course.query.filter(
        Course.topics.any(Topic.name == topic_name)
        )
    return render_template(
        "course/courses_in_topic.html",
        page_title=page_title,
        auth_btns=auth_btns,
        courses_in_topic=courses_in_topic,
        topic_name=topic_name
    )


@course_blueprint.route("/<int:course_id>")
@login_required
def lessons_in_course(course_id):
    page_title = f"{Course.query.get(course_id).title} - lessons"
    auth_btns = get_auth_navbar_btn()
    lessons_in_course = Lesson.query.join(Course).filter(
        Course.id == Lesson.course
        ).filter(Course.id == course_id).all()
    return render_template(
        "course/lessons_in_course.html",
        page_title=page_title,
        auth_btns=auth_btns,
        lessons_in_course=lessons_in_course
    )
