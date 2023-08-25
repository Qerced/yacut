from flask import jsonify, request

from settings import EMPTY_REQUEST_MESSAGE, ID_NOT_FOUND

from . import app
from .error_handler import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    custom_id = data.get('custom_id', '')
    original_link = data.get('url', '')
    url = URLMap.get_or_create(
        original=original_link,
        short=custom_id
    )
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url = URLMap.get_url(short=short_id)
    if url is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, 404)
    return jsonify({'url': url.original})
