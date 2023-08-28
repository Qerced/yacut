import os
import re
import string


DATA_REQUIRED_MESSAGE = '"url" является обязательным полем!'
URL_VALIDATOR_MESSAGE = 'Запрещенные символы'
URL_LEN_MESSAGE = 'Недопустимая длина для длинной ссылки'
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
EXIST_SHORT_MESSAGE_API = 'Имя "{short_name}" уже занято.'
GENERATE_SHORT_ERROR = ('Не удалось сгенерировать короткую'
                        'ссылку, попробуйте еще раз.')
VALID_CHARACTERS = string.ascii_letters + string.digits
PATTERN_FOR_SHORT = f'^[{re.escape(VALID_CHARACTERS)}]+$'
SHORT_MAX_LEN = 16
ORIGINAL_MAX_LEN = 2083
NUMBER_OF_RECEIPTS = 10
LEN_RANDOM_SHORT = 6
URL_VIEW = 'url_view'
CREATE_LINK_VIEW = 'create_link'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='jFXxMHdOIgmzWmrR8i0P0O8HTg3DY2MU'
    )
