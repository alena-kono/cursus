from flask import Blueprint, render_template
from flask_login import current_user

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/")
def index():
    page_title = "Cursus - Home page"
    blocks_to_display = [
        "Topics",
        "Courses"
    ]
    return render_template(
        "home/index.html",
        page_title=page_title,
        blocks=blocks_to_display,
        current_user=current_user
    )


@home_blueprint.route("/plans/")
def plans():
    page_title = "Plans for the project"
    return render_template(
        "plans.html",
        page_title=page_title,
    )
