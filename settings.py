import os
import re


DATAREQUIRED_MESSAGE = '"url" является обязательным полем!'
URLVALIDATOR_MESSAGE = 'Запрещенные символы'
URL_LEN_MESSAGE = 'Недопустимая длина для длинной ссылки'
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
EXIST_SHORT_MESSAGE_API = 'Имя "{short_name}" уже занято.'
EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
SHORT_NOT_FOUND = 'Указанный id не найден'
DONE_LINK_MESSAGE = 'Ваша новая ссылка готова:'
REGEX_FOR_SHORT = re.compile(r'^[a-zA-Z0-9]*$')
SHORT_MAX_LEN = 16
ORIGINAL_MAX_LEN = 2083
NUMBER_OF_RECEIPTS = 10
LEN_RANDOM_SHORT = 6
INDEX_VIEW = 'index_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='jFXxMHdOIgmzWmrR8i0P0O8HTg3DY2MU'
    )
