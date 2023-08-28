import re
from datetime import datetime
from random import choices

from flask import url_for

from settings import (EXIST_SHORT_MESSAGE_API, GENERATE_SHORT_ERROR,
                      INDEX_VIEW, INVALID_SHORT_MESSAGE, LEN_RANDOM_SHORT,
                      NUMBER_OF_RECEIPTS, ORIGINAL_MAX_LEN, PATTERN_FOR_SHORT,
                      SHORT_MAX_LEN, URL_LEN_MESSAGE)
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
            # У меня не работает по-другому
            short_link=url_for(INDEX_VIEW, _external=True) + self.short)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original_link, custom_id):
        # Вы же сами говорили перенести проверки сюда
        if not ORIGINAL_MAX_LEN >= len(original_link):
            raise InvalidDataError(URL_LEN_MESSAGE)
        if not custom_id:
            custom_id = URLMap.get_unique_short_id(original_link)
        if not LEN_RANDOM_SHORT >= len(custom_id):
            raise InvalidDataError(INVALID_SHORT_MESSAGE)
        if re.fullmatch(PATTERN_FOR_SHORT, custom_id) is None:
            raise InvalidDataError(INVALID_SHORT_MESSAGE)
        if URLMap.get(short=custom_id):
            raise InvalidDataError(
                EXIST_SHORT_MESSAGE_API.format(short_name=custom_id)
            )
        url_map = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_unique_short_id(original_link):
        for _ in range(NUMBER_OF_RECEIPTS):
            custom_id = ''.join(
                choices(
                    list(''.join(re.findall(PATTERN_FOR_SHORT,
                                            original_link))),
                    k=LEN_RANDOM_SHORT
                )
            )
            if URLMap.get(custom_id) is None:
                return custom_id
        raise InvalidDataError(GENERATE_SHORT_ERROR)
