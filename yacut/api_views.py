from flask import jsonify, request

from . import app, db
from settings import ACCEPTED_SYMBOLS
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import (MUST_SET_REQUIRED_FIELD, REQUEST_IS_NONE, URL_NOT_EXISTS,
                        ERROR_400, NOT_EXISTS_404, STATUS_OK_200, CREATED_201,
                        UNEXPECTED_NAME, URL_ALREADY_EXISTS)


@app.route('/api/id/', methods=['POST'])
def assigning_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(REQUEST_IS_NONE, ERROR_400)
    if 'url' not in data:
        raise InvalidAPIUsage(MUST_SET_REQUIRED_FIELD.format(must_set='"url"'), ERROR_400)
    if 'custom_id' in data:
        short = data['custom_id']
        if len(short) > 16 or any(
                char not in set(ACCEPTED_SYMBOLS) for char in short
        ):
            raise InvalidAPIUsage(UNEXPECTED_NAME, ERROR_400)
    else:
        short = URLMap.generate_unique_short_id()
    if URLMap.query.filter_by(short=short).first() is not None:
        raise InvalidAPIUsage(URL_ALREADY_EXISTS, ERROR_400)
    urls = URLMap()
    urls.original = data['url']
    urls.short = short
    db.session.add(urls)
    db.session.commit()
    return jsonify(urls.to_dict()), CREATED_201


@app.route('/api/id/<string:short>/', methods=['GET'])
def redirect_to_url_api(short):
    urls = URLMap.query.filter_by(short=short).first()
    if urls is None:
        raise InvalidAPIUsage(URL_NOT_EXISTS, NOT_EXISTS_404)
    return jsonify(urls.to_dict(is_get=True)), STATUS_OK_200
