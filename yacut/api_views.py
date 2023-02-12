from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import (get_unique_short_id, is_not_uniq_short,
                    is_not_valid_short_id, is_not_valid_url)


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    data = request.get_json()
    url = data.get('url')
    if not url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if is_not_valid_url(url):
        raise InvalidAPIUsage('Поле "url" содержит некорректную ссылку')

    custom_id = data.get('custom_id')
    if custom_id is not None and custom_id != '':
        if is_not_uniq_short(custom_id):
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

        if is_not_valid_short_id(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')

    urlmap = URLMap(original=url,
                    short=data.get('custom_id') or get_unique_short_id())
    db.session.add(urlmap)
    db.session.commit()

    return jsonify({
        'url': urlmap.original,
        'short_link': request.host_url + urlmap.short}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_full_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
