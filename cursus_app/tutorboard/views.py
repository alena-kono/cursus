from cursus_app.course.decorators import tutor_required
from cursus_app.course.forms import NewCourseForm
from cursus_app.course.models import Course
from cursus_app.lesson.forms import NewLessonForm
from cursus_app.lesson.models import Lesson
from cursus_app.utils import get_validation_errors
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required

tutorboard_blueprint = Blueprint(
    "tutorboard",
    __name__,
    url_prefix="/tutorboard"
    )


@tutorboard_blueprint.errorhandler(404)
def page_not_found(error):
    page_title = "Page not found"
    return render_template(
        "404.html",
        page_title=page_title
        )


@tutorboard_blueprint.route("/")
@tutorboard_blueprint.route("/courses")
@login_required
def index():
    page_title = "Tutorboard - Cursus"
    all_courses = Course.get_courses_by_tutor(
        tutor_id=current_user.id,
        sort_by_published_at=False
    )
    return render_template(
        "tutorboard/index.html",
        page_title=page_title,
        current_user=current_user,
        courses=all_courses
    )


@tutorboard_blueprint.route("/publish-course", methods=["POST"])
@login_required
def publish_course():
    course_id = request.form.get("course_id")
    if course_id:
        course = Course.query.get(course_id)
        course.publish()
        flash(
            message=f"Course {course.title} has been successfully published",
            category="success")
    else:
        flash(
            message=f"Course {course.title} has not been published",
            category="warning"
        )
    return redirect(url_for("tutorboard.index"))


@tutorboard_blueprint.route("/create-course/")
@login_required
def create_course():
    page_title = "Create new course - Cursus"
    form = NewCourseForm()
    return render_template(
        "tutorboard/create_course.html",
        page_title=page_title,
        current_user=current_user,
        form=form
    )


@tutorboard_blueprint.route("/process-create-course/", methods=["POST"])
@login_required
def process_create_course():
    form = NewCourseForm()
    if form.validate_on_submit():
        new_course = Course()
        new_course.save(
            title=form.title.data,
            description=form.description.data,
            tutor=current_user.id,
            topics=form.topics.data
        )
        flash("New course has been successfully created", "success")
        created_course_id = Course.query.order_by(Course.id.desc()).first().id
        return redirect(url_for(
            "tutorboard.index",
            course_id=created_course_id)
            )
    get_validation_errors(form=form)
    flash("Please, fill in the all fields", "warning")
    return redirect(url_for("tutorboard.create_course"))


@tutorboard_blueprint.route("courses/<int:course_id>/lessons/")
@login_required
@tutor_required
def lessons(course_id: int):
    course = Course.query.get(course_id)
    page_title = f"Tutorboard - '{course.title}' - lessons"
    lessons = course.get_all_lessons()
    return render_template(
        "tutorboard/lessons.html",
        page_title=page_title,
        current_user=current_user,
        lessons=lessons,
        course_id=course_id
    )


@tutorboard_blueprint.route("courses/<int:course_id>/lessons/create-lesson/")
@login_required
@tutor_required
def create_lesson(course_id: int):
    page_title = "Create lesson"
    form = NewLessonForm()
    return render_template(
        "tutorboard/create_lesson.html",
        page_title=page_title,
        current_user=current_user,
        form=form,
        course_id=course_id
    )


@tutorboard_blueprint.route(
    "courses/<int:course_id>/lessons/process-create-lesson/",
    methods=["POST"]
    )
@login_required
@tutor_required
def process_create_lesson(course_id: int):
    form = NewLessonForm()
    if form.validate_on_submit():
        new_lesson = Lesson()
        html_content = form.convert_to_html()
        new_lesson.save(
            title=form.title.data,
            content=html_content,
            course=course_id
        )
        flash(
            message="Lesson has been created",
            category="success"
        )
        return redirect(url_for("tutorboard.lessons", course_id=course_id))
    get_validation_errors(form=form)
    return redirect(url_for("tutorboard.create_lesson"))


@tutorboard_blueprint.route(
    "courses/<int:course_id>/lessons/<int:lesson_id>/"
    )
@login_required
@tutor_required
def lesson(course_id: int, lesson_id: int):
    page_title = "Tutorboard - Lesson"
    lesson = Lesson.query.get(lesson_id)
    form = NewLessonForm()
    if lesson and lesson.course == course_id:
        page_title = f"Lesson {lesson.index} - {lesson.title}"
        return render_template(
            "tutorboard/lesson.html",
            page_title=page_title,
            lesson=lesson,
            course_id=course_id,
            lesson_id=lesson_id,
            form=form
        )
    return abort(404)


@tutorboard_blueprint.route(
    "courses/<int:course_id>/lessons/<int:lesson_id>/update-lesson",
    methods=["POST"]
    )
@login_required
@tutor_required
def update_lesson(course_id: int, lesson_id: int):
    lesson = Lesson.query.get(lesson_id)
    page_title = f"Tutorboard - update lesson #{lesson.index} {lesson.title}"
    if lesson:
        form = NewLessonForm(obj=lesson)
        return render_template(
            "tutorboard/update_lesson.html",
            page_title=page_title,
            lesson=lesson,
            course_id=course_id,
            lesson_id=lesson_id,
            form=form
        )
    return abort(404)


@tutorboard_blueprint.route(
    "courses/<int:course_id>/lessons/<int:lesson_id>/process-update-lesson",
    methods=["POST"]
    )
@login_required
@tutor_required
def process_update_lesson(course_id: int, lesson_id: int):
    lesson = Lesson.query.get(lesson_id)
    page_title = f"Tutorboard - update lesson #{lesson.index} {lesson.title}"
    if lesson:
        form = NewLessonForm(obj=lesson)
        if form.validate_on_submit():
            lesson.save(
                title=form.title.data,
                content=form.content.data,
                course=course_id,
                index=form.index.data
            )
            lesson.update()
            flash(
                "Lesson has been updated",
                "success")
            return redirect(url_for("tutorboard.lessons", course_id=course_id))
        get_validation_errors(form=form)
        return render_template(
            "tutorboard/update_lesson.html",
            page_title=page_title,
            lesson=lesson,
            course_id=course_id,
            lesson_id=lesson_id,
            form=form
        )
    return abort(404)
