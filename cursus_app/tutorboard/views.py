from cursus_app.course.decorators import author_required
from cursus_app.course.forms import NewCourse
from cursus_app.course.models import Course
from cursus_app.lesson.models import Lesson
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

tutorboard_blueprint = Blueprint(
    "tutorboard",
    __name__,
    url_prefix="/tutorboard"
    )


@tutorboard_blueprint.route("/create-course/")
@login_required
def create_course():
    page_title = "Create a course - Cursus"
    new_course_form = NewCourse()
    return render_template(
        "tutorboard/create_course.html",
        page_title=page_title,
        current_user=current_user,
        form=new_course_form
    )


@tutorboard_blueprint.route("/process-create-course/", methods=["POST"])
@login_required
def process_create_course():
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
            "tutorboard.index",
            course_id=created_course_id)
            )
    flash("Please, fill in the all fields", "warning")
    return redirect(url_for("tutorboard.create_course"))


@tutorboard_blueprint.route("/")
@login_required
def index():
    page_title = "Tutorboard - Cursus"
    # lessons_in_course = Lesson.query.join(Course).filter(
    #     Course.id == Lesson.course
    #     ).filter(Course.id == course_id).order_by(Lesson.index.asc()).all()
    # return render_template(
    #     "tutorboard/index.html",
    #     page_title=page_title,
    #     current_user=current_user,
    #     lessons_in_course=lessons_in_course
    # )
    return "All tutorboard courses here"
