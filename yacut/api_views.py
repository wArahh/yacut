import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (DB_ERROR, MAX_SHORT_LENGTH, MUST_SET_REQUIRED_FIELD,
                        REGEXP_ACCEPTED_SYMBOLS, REQUEST_IS_NONE,
                        UNEXPECTED_NAME, URL_ALREADY_EXISTS, URL_NOT_EXISTS)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def assigning_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(REQUEST_IS_NONE, HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(
            MUST_SET_REQUIRED_FIELD.format(
                must_set='"url"'
            ), HTTPStatus.BAD_REQUEST
        )
    if 'custom_id' in data:
        short = data['custom_id']
        if URLMap.get_object(short).first() is not None:
            raise InvalidAPIUsage(URL_ALREADY_EXISTS, HTTPStatus.BAD_REQUEST)
        if (
                len(short) > MAX_SHORT_LENGTH
                or not re.match(REGEXP_ACCEPTED_SYMBOLS, short)
        ):
            raise InvalidAPIUsage(UNEXPECTED_NAME, HTTPStatus.BAD_REQUEST)
        short = URLMap.create_object(data['url'], short).to_dict()
    else:
        short = URLMap.create_object(data['url']).to_dict()
    try:
        return jsonify(short), HTTPStatus.CREATED
    except InvalidAPIUsage as error:
        raise DB_ERROR.format(error=error)


@app.route('/api/id/<string:short>/', methods=['GET'])
def redirect_to_url_api(short):
    try:
        return jsonify(
            URLMap.get_object(short).first_or_404().to_dict(is_get=True)
        ), HTTPStatus.OK
    except Exception:
        raise InvalidAPIUsage(URL_NOT_EXISTS, HTTPStatus.NOT_FOUND)
