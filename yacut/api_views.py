from flask import jsonify, request
from werkzeug.exceptions import BadRequest

from . import app, db
from .models import URLMap
from .views import generate_short_id
from .error_handlers import InvalidAPIUsage

required_field = '{must_set} является обязательным полем!'
url_already_exists = 'Извините, данная ссылка уже используется'
request_is_none = 'Нельзя отправить пустой запрос'


@app.route('/api/id/', methods=['POST'])
def generate_short_id_api():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(request_is_none, 400)
    if 'url' not in data:
        raise InvalidAPIUsage(required_field.format(must_set='\"url\"'), 400)
    if 'custom_id' in data:
        short_link = data['custom_id']
    else:
        short_link = generate_short_id()
    if URLMap.query.filter_by(short=short_link).first() is not None:
        raise InvalidAPIUsage(url_already_exists, 400)
    urls = URLMap()
    urls.original = data['url']
    urls.short = short_link
    db.session.add(urls)
    db.session.commit()
    return jsonify(urls.to_dict()), 201


@app.route('/api/id/<string:short_id>', methods=['GET'])
def redirect_to_url_api(short_id):
    urls = URLMap.query.filter_by(short=short_id).first()
    if urls is None:
        raise BadRequest(requested_variable)
    return jsonify(urls.to_dict()), 200
