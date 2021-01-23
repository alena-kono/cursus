from cursus_app.course.forms import FilterByTutorForm
from cursus_app.course.models import Course, Topic
from cursus_app.lesson.models import Lesson
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

course_blueprint = Blueprint("course", __name__, url_prefix="/courses")


@course_blueprint.route("/")
def index():
    page_title = "Courses - Cursus"
    courses = Course.query.order_by(Course.published_at.desc()).all()
    grouped_by_tutor = Course.query.group_by(Course.author)
    all_topics = Topic.query.all()
    form = FilterByTutorForm()
    form.load_choices(courses=grouped_by_tutor, topics=all_topics)
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
    selected_tutor_id = form.filter_by_tutor.data
    selected_topic_id = form.filter_by_topic.data
    courses = None

    if all((selected_tutor_id, selected_topic_id)):
        courses = Course.query.filter(
            Course.id == selected_tutor_id,
            Topic.id == selected_topic_id,
            ).order_by(Course.published_at.desc()).all()
        if not courses:
            flash("Too many filters", "warning")
            return redirect(url_for("course.index"))
    if selected_tutor_id and not courses:
        courses = Course.get_courses_by_tutor(tutor_id=selected_tutor_id)
    if selected_topic_id and not courses:
        courses = Topic.query.get(selected_topic_id).get_all_courses()

    if courses:
        grouped_by_tutor = Course.query.group_by(Course.author)
        all_topics = Topic.query.all()
        form = FilterByTutorForm()
        form.load_choices(courses=grouped_by_tutor, topics=all_topics)
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


@course_blueprint.route("/topics/<topic_id>")
def courses_in_topic(topic_id):
    topic = Topic.query.get(topic_id)
    if topic:
        page_title = f"{topic.name} - Cursus"
        courses_in_topic = topic.get_all_courses()
        return render_template(
            "course/courses_in_topic.html",
            page_title=page_title,
            current_user=current_user,
            courses_in_topic=courses_in_topic,
            topic=topic
        )
    return abort(404)


@course_blueprint.route("/<int:course_id>")
@course_blueprint.route("/<int:course_id>/lessons/")
@login_required
def lessons_in_course(course_id):
    course = Course.query.get(course_id)
    topics = course.get_all_topics()
    page_title = f"{course.title} - lessons - Cursus"
    lessons_in_course = course.get_all_lessons()
    return render_template(
        "course/lessons_in_course.html",
        page_title=page_title,
        current_user=current_user,
        lessons_in_course=lessons_in_course,
        course_id=course_id,
        topics=topics
    )


@course_blueprint.route(
    "/<int:course_id>/lessons/<int:lesson_id>/"
    )
@login_required
def lesson(course_id: int, lesson_id: int):
    page_title = "Lesson - Cursus"
    lesson = Lesson.query.get(lesson_id)
    if lesson:
        page_title = f"Lesson {lesson.index} - {lesson.title} - Cursus"
        return render_template(
            "course/lesson.html",
            page_title=page_title,
            lesson=lesson,
            course_id=course_id,
            lesson_id=lesson_id,
        )
    return abort(404)
