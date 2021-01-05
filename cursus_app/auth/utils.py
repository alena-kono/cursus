from collections import namedtuple

from flask import url_for
from flask_login import current_user


def get_auth_navbar_btn() -> tuple:
    auth_navbar_btn = namedtuple("auth_navbar_btn", ["btn", "link"])
    auth_btn_1 = auth_navbar_btn(
        btn="Log In",
        link=url_for("auth.login")
    )
    auth_btn_2 = auth_navbar_btn(
        btn="Sign Up",
        link=url_for("auth.signup")
    )
    if current_user.is_authenticated:
        auth_btn_1 = auth_navbar_btn(
            btn=f"{current_user.username} is logged in",
            link="#"
        )
        auth_btn_2 = auth_navbar_btn(
            btn="Log Out",
            link=url_for("auth.logout")
        )
    return (auth_btn_1, auth_btn_2)
