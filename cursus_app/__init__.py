from flask import Flask
from cursus_app.db import db
from cursus_app.home.views import home_blueprint


def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder="static",
        static_url_path="/"
        )
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.register_blueprint(home_blueprint)

    return app
