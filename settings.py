import os


DATAREQUIRED_MESSAGE = '"url" является обязательным полем!'
URLVALIDATOR_MESSAGE = 'Запрещенные символы'
URL_LEN_MESSAGE = 'Недопустимая длина для длинной ссылки'
CUSTOMID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
EXIST_SHORT_MESSAGE = 'Имя {short_name} уже занято!'
EXIST_SHORT_MESSAGE_MODEL = 'Имя "{short_name}" уже занято.'
EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
ID_NOT_FOUND = 'Указанный id не найден'
DONE_LINK_MESSAGE = 'Ваша новая ссылка готова:'
SUBMIT_BUTTON = 'Создать'
REGEX_CUSTOMID_FORM = '[A-Za-z0-9]+$'
REGEX_ORIGINAL = (
    r"^[a-z]+://"
    r"(?P<host>[^\/\?:]+)"
    r"(?P<port>:[0-9]+)?"
    r"(?P<path>\/.*?)?"
    r"(?P<query>\?.*)?$"
)
REGEX_CUSTOMID = r'[^a-zA-Z0-9]'
REGEX_CUSTOMID_VALIDATOR = r'[A-Za-z0-9]+$'
SHORT_MIN_LEN = 1
SHORT_MAX_LEN = 16
ORIGINAL_MIN_LEN = 17
ORIGINAL_MAX_LEN = 356
NUMBER_OF_RECEIPTS = 10
LEN_RANDOM_SHORT = 6


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='jFXxMHdOIgmzWmrR8i0P0O8HTg3DY2MU'
    )
