from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import (DATAREQUIRED_MESSAGE, INVALID_SHORT_MESSAGE,
                      ORIGINAL_MAX_LEN, REGEX_FOR_SHORT, SHORT_MAX_LEN,
                      URLVALIDATOR_MESSAGE)
from .models import URLMap

LABEL_ORIGINAL = 'Длинная ссылка'
LABEL_SHORT = 'Ваш вариант короткой ссылки'
EXIST_SHORT_MESSAGE = 'Имя {short_name} уже занято!'
SUBMIT_BUTTON = 'Создать'


class YacutForm(FlaskForm):
    original_link = URLField(
        LABEL_ORIGINAL,
        validators=[
            DataRequired(message=DATAREQUIRED_MESSAGE),
            Length(max=ORIGINAL_MAX_LEN),
            URL(message=URLVALIDATOR_MESSAGE)
        ]
    )
    custom_id = URLField(
        LABEL_SHORT,
        validators=[
            Optional(),
            Length(max=SHORT_MAX_LEN,
                   message=INVALID_SHORT_MESSAGE),
            Regexp(regex=REGEX_FOR_SHORT, message=INVALID_SHORT_MESSAGE)
        ]
    )
    submit = SubmitField(SUBMIT_BUTTON)

    def validate_custom_id(form, field):
        if URLMap.get(short=field.data):
            raise ValidationError(
                EXIST_SHORT_MESSAGE.format(short_name=field.data)
            )
