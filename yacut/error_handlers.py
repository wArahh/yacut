from http import HTTPStatus

from flask import jsonify, render_template
from sqlalchemy import exc

from . import app, db
from .constants import DB_ERROR


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


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    try:
        return render_template('404.html'), HTTPStatus.NOT_FOUND
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return InvalidAPIUsage(
            DB_ERROR.format(error=e), HTTPStatus.INTERNAL_SERVER_ERROR
        )
