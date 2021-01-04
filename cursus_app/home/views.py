from flask import Blueprint, render_template

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
        blocks=blocks_to_display
    )
