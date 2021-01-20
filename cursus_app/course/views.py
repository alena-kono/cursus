from cursus_app.course.forms import FilterByTutorForm
from cursus_app.course.models import Course, Topic
from cursus_app.lesson.models import Lesson
from cursus_app.user.models import User
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

course_blueprint = Blueprint("course", __name__, url_prefix="/courses")


@course_blueprint.route("/")
def index():
    page_title = "Courses - Cursus"
    courses = Course.query.order_by(Course.published_at.desc()).all()
    grouped_by_tutor = Course.query.group_by(Course.author)
    form = FilterByTutorForm()
    form.filter_by.choices = form.get_all_tutors(grouped_by_tutor)
    return render_template(
        "course/courses.html",
        page_title=page_title,
        current_user=current_user,
        courses=courses,
        form=form
    )


@course_blueprint.route("/process-filter", methods=["POST"])
def process_filter():
    page_title = "Courses - Cursus"
    form = FilterByTutorForm()
    filter_by = form.filter_by.data
    if filter_by:
        courses = Course.query.filter(
            Course.author == filter_by).order_by(
                Course.published_at.desc()).all()
        tutor = User.query.get(filter_by).username
        page_title = f"Courses by {tutor} - Cursus"
        form = FilterByTutorForm()
        grouped_by_tutor = Course.query.group_by(Course.author)
        form.filter_by.choices = form.get_all_tutors(grouped_by_tutor)
        return render_template(
            "course/courses.html",
            page_title=page_title,
            current_user=current_user,
            courses=courses,
            form=form
        )
    return redirect(url_for("course.index"))


@course_blueprint.route("/topics/")
def topics():
    page_title = "Topics - Cursus"
    all_topics = Topic.query.all()
    return render_template(
        "course/topics.html",
        page_title=page_title,
        current_user=current_user,
        topics=all_topics
    )


@course_blueprint.route("/topics/<topic_name>")
def courses_in_topic(topic_name):
    page_title = f"{topic_name} - Cursus"
    courses_in_topic = Course.query.filter(
        Course.topics.any(Topic.name == topic_name)
        )
    return render_template(
        "course/courses_in_topic.html",
        page_title=page_title,
        current_user=current_user,
        courses_in_topic=courses_in_topic,
        topic_name=topic_name
    )


@course_blueprint.route("/<int:course_id>")
@login_required
def lessons_in_course(course_id):
    page_title = f"{Course.query.get(course_id).title} - lessons - Cursus"
    lessons_in_course = Lesson.query.join(Course).filter(
        Course.id == Lesson.course
        ).filter(Course.id == course_id).all()
    return render_template(
        "course/lessons_in_course.html",
        page_title=page_title,
        current_user=current_user,
        lessons_in_course=lessons_in_course
    )
