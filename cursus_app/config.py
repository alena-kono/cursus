import pathlib

SQLALCHEMY_TRACK_MODIFICATIONS = False

basedir = pathlib.Path(__file__).parents[1]
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(pathlib.Path.joinpath(
    basedir,
    'cursus_app.db'
    ))

SECRET_KEY = pathlib.os.getenv("FLASK_SECRET_KEY")
