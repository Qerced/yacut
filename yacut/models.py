import re
from datetime import datetime
from random import choices

from flask import url_for

from settings import (CUSTOMID_MESSAGE, DATAREQUIRED_MESSAGE,
                      EXIST_SHORT_MESSAGE_MODEL, LEN_RANDOM_SHORT,
                      NUMBER_OF_RECEIPTS, ORIGINAL_MAX_LEN, ORIGINAL_MIN_LEN,
                      REGEX_CUSTOMID, REGEX_CUSTOMID_VALIDATOR, REGEX_ORIGINAL,
                      SHORT_MAX_LEN, SHORT_MIN_LEN, URL_LEN_MESSAGE,
                      URLVALIDATOR_MESSAGE)

from . import db
from .error_handler import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short)

    @classmethod
    def get_or_create(cls, **kwargs):
        original_link, custom_id = kwargs.values()
        url = cls.get_url(original=original_link)
        if url is None:
            url = cls.create(original_link, custom_id)
        else:
            url = url.update_custom_id(custom_id)
        return url

    @classmethod
    def get_url(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def create(cls, original_link, custom_id):
        original_link, custom_id = cls.validate(original_link, custom_id)
        url = cls(original=original_link, short=custom_id)
        db.session.add(url)
        db.session.commit()
        return url

    def update_custom_id(self, custom_id):
        if custom_id:
            self.short = self.validate_custom_id(custom_id)
        else:
            self.short = self.get_unique_short_id(self.original)
        db.session.commit()
        return self

    @classmethod
    def validate(cls, original_link, custom_id=None):
        cls.validate_original_link(original_link)
        if custom_id:
            cls.validate_custom_id(custom_id)
        else:
            custom_id = cls.get_unique_short_id(original_link)
        return original_link, custom_id

    @classmethod
    def validate_custom_id(cls, custom_id):
        if cls.get_url(short=custom_id):
            raise InvalidAPIUsage(
                EXIST_SHORT_MESSAGE_MODEL.format(short_name=custom_id)
            )
        if not (SHORT_MAX_LEN >= len(custom_id) >= SHORT_MIN_LEN):
            raise InvalidAPIUsage(CUSTOMID_MESSAGE)
        if re.compile(REGEX_CUSTOMID_VALIDATOR).match(custom_id or '') is None:
            raise InvalidAPIUsage(CUSTOMID_MESSAGE)

    def validate_original_link(original_link):
        if not original_link:
            raise InvalidAPIUsage(DATAREQUIRED_MESSAGE)
        if not (ORIGINAL_MAX_LEN >= len(original_link) >= ORIGINAL_MIN_LEN):
            raise InvalidAPIUsage(URL_LEN_MESSAGE)
        if re.compile(REGEX_ORIGINAL).match(original_link or '') is None:
            raise InvalidAPIUsage(URLVALIDATOR_MESSAGE)

    @classmethod
    def get_unique_short_id(cls, original_link):
        for _ in range(NUMBER_OF_RECEIPTS):
            custom_id = cls.random_url(original_link)
            if cls.get_url(short=custom_id) is None:
                break
        return custom_id

    def random_url(original_link):
        return ''.join(choices(list(re.sub(
            REGEX_CUSTOMID, '', ''.join(original_link.split('/'))
        )), k=LEN_RANDOM_SHORT))
