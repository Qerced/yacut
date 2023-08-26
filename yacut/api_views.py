from http import HTTPStatus

from flask import jsonify, request

from settings import EMPTY_REQUEST_MESSAGE, SHORT_NOT_FOUND
from . import app
from .error_handler import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    custom_id = data.get('custom_id')
    original_link = data.get('url')
    URLMap.validate_original(original_link)
    if custom_id:
        URLMap.validate_short(custom_id)
    else:
        custom_id = URLMap.get_unique_short_id(original_link)
    url_map = URLMap.create(
        original_link=original_link,
        custom_id=custom_id,
    )
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url_map = URLMap.get(short=short_id)
    if url_map is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
