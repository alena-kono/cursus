from flask import flash
from flask_wtf import FlaskForm


def get_validation_errors(form: FlaskForm) -> flash:
    for field, errors in form.errors.items():
        for error in errors:
            field_label = getattr(form, field).label.text
            flash(
                f"Field '{field_label}' is incorrect - {error}",
                "warning"
                )
