from flask import url_for

from .constants import REDIRECT_URL


def get_short_link(short):
    return url_for(
        REDIRECT_URL,
        short=short,
        _external=True
    )
