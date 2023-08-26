import re
from datetime import datetime
from random import choices

from flask import url_for

from settings import (DATAREQUIRED_MESSAGE, EXIST_SHORT_MESSAGE_API,
                      INDEX_VIEW, INVALID_SHORT_MESSAGE, LEN_RANDOM_SHORT,
                      NUMBER_OF_RECEIPTS, ORIGINAL_MAX_LEN, REGEX_FOR_ORIGINAL,
                      REGEX_FOR_SHORT, SHORT_MAX_LEN, URL_LEN_MESSAGE,
                      URLVALIDATOR_MESSAGE)
from . import db
from .error_handler import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LEN), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LEN))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(INDEX_VIEW, _external=True) + self.short)

    @staticmethod
    def get(short=None):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original_link, custom_id):
        url = URLMap(original=original_link, short=custom_id)
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def get_unique_short_id(original_link):
        for _ in range(NUMBER_OF_RECEIPTS):
            custom_id = URLMap.random_url(original_link)
            if URLMap.get(short=custom_id) is None:
                break
        return custom_id

    @staticmethod
    def random_url(original_link):
        return ''.join(choices(list(re.sub(
            REGEX_FOR_SHORT, '', ''.join(original_link.split('/'))
        )), k=LEN_RANDOM_SHORT))

    @staticmethod
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

    @staticmethod
    def validate_short(custom_id):
        if not (URLMap.short.type.length >= len(custom_id)):
            raise InvalidAPIUsage(INVALID_SHORT_MESSAGE)
        if re.compile(REGEX_FOR_SHORT).match(custom_id or '') is None:
            raise InvalidAPIUsage(INVALID_SHORT_MESSAGE)
        if URLMap.get(short=custom_id):
            raise InvalidAPIUsage(
                EXIST_SHORT_MESSAGE_API.format(short_name=custom_id)
            )
