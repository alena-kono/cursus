from cursus_app.auth.utils import get_auth_navbar_btn
from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/")
def index():
    page_title = "Cursus - Home page"
    blocks_to_display = [
        "Topics",
        "Courses"
    ]
    auth_btn = get_auth_navbar_btn()
    return render_template(
        "home/index.html",
        page_title=page_title,
        blocks=blocks_to_display,
        auth_btn=auth_btn
    )
