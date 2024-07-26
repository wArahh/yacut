from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import MUST_SET_REQUIRED_FIELD, REQUEST_IS_NONE, URL_NOT_EXISTS
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
    short = data.get('custom_id')
    return jsonify(
        URLMap.create(
            data['url'], short, is_api=True
        ).to_dict() if short else URLMap.create(
            data['url'], is_api=True
        ).to_dict()
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def redirect_to_url_api(short):
    urlmap = URLMap.get_object(short)
    if urlmap is not None:
        return jsonify(
            urlmap.to_dict(is_get=True)
        ), HTTPStatus.OK
    raise InvalidAPIUsage(URL_NOT_EXISTS, HTTPStatus.NOT_FOUND)
