import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (
    CANNOT_BE_MORE_MAX_ORIGINAL, MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH, MUST_SET_REQUIRED_FIELD,
    REGEXP_ACCEPTED_SYMBOLS, REQUEST_IS_NONE,
    UNEXPECTED_NAME, URL_ALREADY_EXISTS, URL_NOT_EXISTS
)
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
    original = data['url']
    short = data.get('custom_id')
    if short is None:
        short = URLMap.generate_unique_short()
    if (
            len(short) > MAX_SHORT_LENGTH
            or not re.match(REGEXP_ACCEPTED_SYMBOLS, short)
    ):
        raise InvalidAPIUsage(UNEXPECTED_NAME, HTTPStatus.BAD_REQUEST)
    if len(original) > MAX_ORIGINAL_LENGTH:
        raise ValueError(CANNOT_BE_MORE_MAX_ORIGINAL)
    if URLMap.get(short) is not None:
        raise InvalidAPIUsage(
            URL_ALREADY_EXISTS, HTTPStatus.BAD_REQUEST
        )
    try:
        return jsonify(URLMap.create(
            original, short
        ).to_dict()), HTTPStatus.CREATED
    except InvalidAPIUsage as error:
        raise error


@app.route('/api/id/<string:short>/', methods=['GET'])
def redirect_to_url_api(short):
    url_map = URLMap.get(short)
    if url_map is not None:
        return jsonify(
            url_map.to_dict(is_get=True)
        ), HTTPStatus.OK
    raise InvalidAPIUsage(URL_NOT_EXISTS, HTTPStatus.NOT_FOUND)
