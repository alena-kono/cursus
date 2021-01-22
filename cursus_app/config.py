import pathlib

import dotenv

SQLALCHEMY_TRACK_MODIFICATIONS = False

basedir = pathlib.Path(__file__).parents[1]
SQLALCHEMY_DATABASE_URI = (
    dotenv.get_key(".env", "SQLALCHEMY_DATABASE_URI")
    ) or ("sqlite:///" + str(pathlib.Path.joinpath(
        basedir,
        "cursus_app.db")
    ))

SECRET_KEY = dotenv.get_key(".env", "FLASK_SECRET_KEY")
