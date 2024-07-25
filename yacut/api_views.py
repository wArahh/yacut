from flask import jsonify, request

from . import app
from .constants import (CREATED_201, BAD_REQUEST_400, MUST_SET_REQUIRED_FIELD,
                        REQUEST_IS_NONE, STATUS_OK_200)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def assigning_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(REQUEST_IS_NONE, BAD_REQUEST_400)
    if 'url' not in data:
        raise InvalidAPIUsage(
            MUST_SET_REQUIRED_FIELD.format(must_set='"url"'), BAD_REQUEST_400
        )
    if 'custom_id' in data:
        short = data['custom_id']
    else:
        short = URLMap.generate_unique_short_id()
    return jsonify(
        URLMap.check_and_create(data['url'], short).to_dict()
    ), CREATED_201


@app.route('/api/id/<string:short>/', methods=['GET'])
def redirect_to_url_api(short):
    return jsonify(
        URLMap.get_object(short).to_dict(is_get=True)
    ), STATUS_OK_200
