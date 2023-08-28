from http import HTTPStatus

from flask import jsonify, request

from settings import DATA_REQUIRED_MESSAGE, ORIGINAL_MAX_LEN, URL_LEN_MESSAGE
from . import app
from .error_handler import InvalidAPIUsage, InvalidDataError
from .models import URLMap

EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
SHORT_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    custom_id = data.get('custom_id')
    original_link = data.get('url')
    if not original_link:
        raise InvalidAPIUsage(DATA_REQUIRED_MESSAGE)
    if ORIGINAL_MAX_LEN < len(original_link):
        raise InvalidDataError(URL_LEN_MESSAGE)
    try:
        return jsonify(URLMap.create(original_link=original_link,
                                     custom_id=custom_id
                                     ).to_dict()), HTTPStatus.CREATED
    except InvalidDataError as error:
        raise InvalidAPIUsage(*error.args)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url_map = URLMap.get(short=short_id)
    if url_map is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
