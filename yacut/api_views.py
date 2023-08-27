from http import HTTPStatus

from flask import jsonify, request

from settings import EMPTY_REQUEST_MESSAGE, SHORT_NOT_FOUND
from . import app
from .error_handler import InvalidAPIUsage, InvalidDataError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    custom_id = data.get('custom_id')
    original_link = data.get('url')
    try:
        url_map = URLMap.create(
            original_link=original_link,
            custom_id=custom_id,
        )
    except InvalidDataError as error:
        raise InvalidAPIUsage(error.message)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url_map = URLMap.get(short=short_id)
    if url_map is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
