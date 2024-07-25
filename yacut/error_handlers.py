from flask import jsonify, render_template

from .constants import NOT_EXISTS_404
from . import app


class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(NOT_EXISTS_404)
def page_not_found(error):
    return render_template('404.html'), NOT_EXISTS_404
