from flask import jsonify, request
from werkzeug.exceptions import BadRequest

from . import app, db
from .models import URLMap
from .views import generate_short_id
from .error_handlers import InvalidAPIUsage
from .utils import ACCEPTED_SYMBOLS

required_field = '{must_set} является обязательным полем!'
url_already_exists = 'Предложенный вариант короткой ссылки уже существует.'
request_is_none = 'Нельзя отправить пустой запрос'
unexpected_name = 'Указано недопустимое имя для короткой ссылки'
url_not_exists = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def generate_short_id_api():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(request_is_none, 400)
    if 'url' not in data:
        raise InvalidAPIUsage(required_field.format(must_set='\"url\"'), 400)
    if 'custom_id' in data:
        short_link = data['custom_id']
        if any(char not in set(ACCEPTED_SYMBOLS) for char in short_link):
            raise InvalidAPIUsage(unexpected_name, 400)
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
        raise InvalidAPIUsage(url_not_exists, 404)
    return jsonify(urls.to_dict(is_get=True)), 200
