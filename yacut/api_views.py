import re
from http import HTTPStatus

from flask import jsonify, request

from settings import (DATAREQUIRED_MESSAGE, EMPTY_REQUEST_MESSAGE,
                      EXIST_SHORT_MESSAGE_API, INVALID_SHORT_MESSAGE,
                      REGEX_FOR_ORIGINAL, REGEX_FOR_SHORT, SHORT_NOT_FOUND,
                      URL_LEN_MESSAGE, URLVALIDATOR_MESSAGE)

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
    validate_original(original_link)
    if custom_id:
        validate_short(custom_id)
    else:
        custom_id = URLMap.get_unique_short_id(original_link)
    urlmap = URLMap.create(
        original_link=original_link,
        custom_id=custom_id,
    )
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url = URLMap.get(short=short_id)
    if url is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original})


def validate_original(original_link):
    if not original_link:
        raise InvalidAPIUsage(DATAREQUIRED_MESSAGE)
    if not (
        URLMap.original.type.length >=
        len(original_link) >
        URLMap.short.type.length
    ):
        raise InvalidAPIUsage(URL_LEN_MESSAGE)
    if re.compile(REGEX_FOR_ORIGINAL).match(original_link or '') is None:
        raise InvalidAPIUsage(URLVALIDATOR_MESSAGE)


def validate_short(custom_id):
    if not (URLMap.short.type.length >= len(custom_id)):
        raise InvalidAPIUsage(INVALID_SHORT_MESSAGE)
    if re.compile(REGEX_FOR_SHORT).match(custom_id or '') is None:
        raise InvalidAPIUsage(INVALID_SHORT_MESSAGE)
    if URLMap.get(short=custom_id):
        raise InvalidAPIUsage(
            EXIST_SHORT_MESSAGE_API.format(short_name=custom_id)
        )
