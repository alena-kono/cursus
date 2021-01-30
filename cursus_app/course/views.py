from cursus_app.course.forms import FilterByTutorAndTopicForm
from cursus_app.course.models import Course, Topic
from cursus_app.lesson.models import Lesson
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

course_blueprint = Blueprint("course", __name__, url_prefix="/courses")


@course_blueprint.errorhandler(404)
def page_not_found(error):
    page_title = "Page not found"
    return render_template(
        "404.html",
        page_title=page_title
        )


@course_blueprint.route("/")
def index():
    page_title = "Courses"
    courses = Course.get_all_published_courses()
    tutors = Course.get_tutors()
    all_topics = Topic.query.all()
    form = FilterByTutorAndTopicForm()
    form.load_choices(tutors=tutors, topics=all_topics)
    return render_template(
        "course/courses.html",
        page_title=page_title,
        current_user=current_user,
        courses=courses,
        form=form
    )


@course_blueprint.route("/process-filter", methods=["POST"])
def process_filter():
    page_title = "Courses"
    form = FilterByTutorAndTopicForm()
    selected_tutor_id = form.filter_by_tutor.data
    selected_topic_id = form.filter_by_topic.data
    courses = None

    if all((selected_tutor_id, selected_topic_id)):
        courses = Course.filter_by_tutor_and_topic(
            tutor_id=selected_tutor_id,
            topic_id=selected_topic_id
        )
        if not courses:
            flash("Too many filters", "warning")
            return redirect(url_for("course.index"))
    if selected_tutor_id and not courses:
        courses = Course.get_courses_by_tutor(tutor_id=selected_tutor_id)
    if selected_topic_id and not courses:
        courses = Topic.query.get(selected_topic_id).get_all_courses()

    if courses:
        tutors = Course.get_tutors()
        all_topics = Topic.query.all()
        form = FilterByTutorAndTopicForm()
        form.load_choices(tutors=tutors, topics=all_topics)
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
    page_title = "Topics"
    all_topics = Topic.query.all()
    return render_template(
        "course/topics.html",
        page_title=page_title,
        current_user=current_user,
        topics=all_topics
    )


@course_blueprint.route("/<int:course_id>")
@course_blueprint.route("/<int:course_id>/lessons/")
@login_required
def lessons_in_course(course_id):
    course = Course.query.get(course_id)
    if course:
        topics = course.get_all_topics()
        page_title = f"Course {course.title} - lessons"
        lessons = course.get_all_lessons()
        return render_template(
            "course/lessons_in_course.html",
            page_title=page_title,
            current_user=current_user,
            lessons_in_course=lessons,
            course_id=course_id,
            topics=topics
        )
    abort(404)


@course_blueprint.route(
    "/<int:course_id>/lessons/<int:lesson_id>/"
    )
@login_required
def lesson(course_id: int, lesson_id: int):
    page_title = "Lesson"
    lesson = Lesson.query.get(lesson_id)
    if lesson and lesson.course == course_id:
        page_title = f"Lesson {lesson.index} - {lesson.title}"
        return render_template(
            "course/lesson.html",
            page_title=page_title,
            lesson=lesson,
            course_id=course_id,
            lesson_id=lesson_id,
        )
    return abort(404)
