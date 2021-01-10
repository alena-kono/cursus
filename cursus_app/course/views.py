from cursus_app.auth.utils import get_auth_navbar_btn
from cursus_app.course.forms import NewCourse
from cursus_app.course.models import Course, Topic
from cursus_app.lesson.models import Lesson
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from cursus_app.course.decorators import author_required

course_blueprint = Blueprint("course", __name__, url_prefix="/courses")


@course_blueprint.route("/")
def index():
    page_title = "Courses - Cursus"
    auth_btns = get_auth_navbar_btn()
    courses = Course.query.order_by(Course.published_at.desc()).all()
    return render_template(
        "course/courses.html",
        page_title=page_title,
        auth_btns=auth_btns,
        courses=courses
    )


@course_blueprint.route("/topics/")
def topics():
    page_title = "Topics - Cursus"
    auth_btns = get_auth_navbar_btn()
    all_topics = Topic.query.all()
    return render_template(
        "course/topics.html",
        page_title=page_title,
        auth_btns=auth_btns,
        topics=all_topics
    )


@course_blueprint.route("/topics/<topic_name>")
def courses_in_topic(topic_name):
    page_title = f"{topic_name} - Cursus"
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
    page_title = f"{Course.query.get(course_id).title} - lessons - Cursus"
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


@course_blueprint.route("/create")
@login_required
def create():
    page_title = "Create a course - Cursus"
    new_course_form = NewCourse()
    auth_btns = get_auth_navbar_btn()
    return render_template(
        "course/create.html",
        page_title=page_title,
        auth_btns=auth_btns,
        form=new_course_form
    )


@course_blueprint.route("/process-create", methods=["POST"])
@login_required
def process_create():
    form = NewCourse()
    if form.validate_on_submit():
        new_course = Course()
        new_course.save(
            title=form.title.data,
            description=form.description.data,
            author=current_user.id
        )
        flash("New course has been successfully created", "success")
        created_course_id = Course.query.order_by(Course.id.desc()).first().id
        return redirect(url_for(
            "course.authorboard",
            course_id=created_course_id)
            )
    flash("Please, fill in the all fields", "warning")
    return redirect(url_for("course.create_course"))


@course_blueprint.route("/<int:course_id>/authorboard/")
@login_required
@author_required
def authorboard(course_id: int):
    page_title = "Authorboard - Cursus"
    auth_btns = get_auth_navbar_btn()
    lessons_in_course = Lesson.query.join(Course).filter(
        Course.id == Lesson.course
        ).filter(Course.id == course_id).order_by(Lesson.index.asc()).all()
    return render_template(
        "course/authorboard.html",
        page_title=page_title,
        auth_btns=auth_btns,
        lessons_in_course=lessons_in_course
    )
