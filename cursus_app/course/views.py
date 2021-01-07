from cursus_app.auth.utils import get_auth_navbar_btn
from cursus_app.course.models import Course
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
