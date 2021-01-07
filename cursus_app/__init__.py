from flask import Flask
from flask_login import LoginManager

from cursus_app.auth.views import auth_blueprint
from cursus_app.course.views import course_blueprint
from cursus_app.db import db
from cursus_app.home.views import home_blueprint
from cursus_app.user.models import User


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        )
    app.config.from_pyfile("config.py")
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.views"
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(course_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
