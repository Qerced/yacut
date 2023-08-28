import re
from datetime import datetime
from random import choices

from flask import url_for

from settings import (EXIST_SHORT_MESSAGE_API, GENERATE_SHORT_ERROR,
                      INVALID_SHORT_MESSAGE, LEN_RANDOM_SHORT,
                      NUMBER_OF_RECEIPTS, ORIGINAL_MAX_LEN, PATTERN_FOR_SHORT,
                      SHORT_MAX_LEN, URL_VIEW, VALID_CHARACTERS)
from . import db
from .error_handler import InvalidDataError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LEN), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LEN))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(URL_VIEW, short_url=self.short, _external=True))

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original_link, custom_id):
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
        elif LEN_RANDOM_SHORT < len(custom_id):
            raise InvalidDataError(INVALID_SHORT_MESSAGE)
        elif re.match(PATTERN_FOR_SHORT, custom_id) is None:
            raise InvalidDataError(INVALID_SHORT_MESSAGE)
        elif URLMap.get(short=custom_id):
            raise InvalidDataError(
                EXIST_SHORT_MESSAGE_API.format(short_name=custom_id)
            )
        url_map = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_unique_short_id():
        for _ in range(NUMBER_OF_RECEIPTS):
            custom_id = ''.join(
                choices(list(VALID_CHARACTERS), k=LEN_RANDOM_SHORT)
            )
            if URLMap.get(custom_id) is None:
                return custom_id
        raise InvalidDataError(GENERATE_SHORT_ERROR)
