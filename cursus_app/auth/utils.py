from collections import namedtuple

from flask import url_for
from flask_login import current_user


def get_auth_navbar_btn() -> namedtuple:
    auth_navbar_btn = namedtuple("auth_navbar_btn", ["btn", "link"])
    current_auth_navbar_btn = auth_navbar_btn(
        btn="Log In",
        link=url_for("auth.login")
    )
    if current_user.is_authenticated:
        current_auth_navbar_btn = auth_navbar_btn(
            btn=f"{current_user.username} is logged in",
            link="#"
        )
    return current_auth_navbar_btn
