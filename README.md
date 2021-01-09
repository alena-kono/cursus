# Cursus

Cursus is a platform for sharing knowledge.
You can easily create your own course and fill it with some lessons or attend another user's course.

## Installation
```
git clone https://github.com/alena-kono/cursus.git
pip install -r requirements.txt
```

## Configuration
Create ```.env``` file at the top level directory of the project and add variables:
```
FLASK_APP = cursus_app
FLASK_ENV = development
FLASK_SECRET_KEY = "YOUR SECRET KEY"
SQLALCHEMY_DATABASE_URI = "LINK TO YOUR SQLITE3 DATABASE"
```
If ```SQLALCHEMY_DATABASE_URI``` is not setup up as environment variable, then sqlite3 database will be created at the top level directory of the project.

## Run
To run development Flask server:
```
flask run
```
