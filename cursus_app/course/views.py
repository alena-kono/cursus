from cursus_app.auth.utils import get_auth_navbar_btn
from cursus_app.course.models import Course, Topic
from flask import Blueprint, flash, redirect, render_template, url_for

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