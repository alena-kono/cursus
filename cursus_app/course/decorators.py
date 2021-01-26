from functools import wraps

from cursus_app.course.models import Course
from flask import current_app, flash, redirect, request, url_for
from flask_login import config, current_user


def tutor_required(func):
    """View decorator that ensures current user to be the tutor
    of the Course with `course_id` before calling the actual view.
    (If they are not, it flashes 'Access denied' warning and redirects
    to 'home.index'page).
    `course_id` parameter should be passed to the actual view,
    otherwise TypeError exception will be raised.

    For example:

        @app.route('/courses/course_id/tutorboard')
        @tutor_required
        def publish_lesson(course_id):
            pass

    It can be convenient to globally turn off authentication when unit testing.
    To enable this, if the application configuration variable `LOGIN_DISABLED`
    is set to `True`, this decorator will be ignored.

    :param func: the view function to decorate
    :type func: function

    :raises TypeError: if `course_id` is not passed in view function

    :returns: decorated view function
    :rtype: function
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        course_id = kwargs.get("course_id")
        if not course_id:
            raise TypeError(f"{func} missing 1 required positional argument:"
                            "'course_id'")
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        if current_app.config.get("LOGIN_DISABLED"):
            return func(*args, **kwargs)
        current_course = Course.query.get(course_id)
        course_tutor_id = current_course.tutor
        if not current_user.id == course_tutor_id:
            flash(
                "Access denied. You are not the tutor of course "
                f"'{current_course.title}'",
                "danger"
                )
            return redirect(url_for("home.index"))
        return func(*args, **kwargs)
    return decorated_view
