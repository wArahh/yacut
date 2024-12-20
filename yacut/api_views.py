from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import MUST_SET_REQUIRED_FIELD, REQUEST_IS_NONE, URL_NOT_EXISTS
from .error_handlers import InvalidAPIUsage
from .exceptions import (
    DuplicateShortURLError, ShortURLError, TooManyAttemptsError
)
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
    try:
        return jsonify(URLMap.create(
            original=data['url'],
            short=data.get('custom_id'),
        ).to_dict()), HTTPStatus.CREATED
    except (
        ShortURLError,
        DuplicateShortURLError,
        TooManyAttemptsError
    ) as error:
        raise InvalidAPIUsage(str(error), HTTPStatus.BAD_REQUEST)


@app.route('/api/id/<string:short>/', methods=['GET'])
def redirect_to_url_api(short):
    url_map = URLMap.get(short)
    if url_map is not None:
        return jsonify(
            url_map.to_dict(is_get=True)
        ), HTTPStatus.OK
    raise InvalidAPIUsage(URL_NOT_EXISTS, HTTPStatus.NOT_FOUND)
