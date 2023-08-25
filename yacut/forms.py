from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import (CUSTOMID_MESSAGE, DATAREQUIRED_MESSAGE,
                      EXIST_SHORT_MESSAGE, ORIGINAL_MAX_LEN, ORIGINAL_MIN_LEN,
                      REGEX_CUSTOMID_FORM, SHORT_MAX_LEN, SHORT_MIN_LEN,
                      SUBMIT_BUTTON, URLVALIDATOR_MESSAGE)

from .models import URLMap


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message=DATAREQUIRED_MESSAGE),
            Length(ORIGINAL_MIN_LEN, ORIGINAL_MAX_LEN),
            URL(message=URLVALIDATOR_MESSAGE)
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(SHORT_MIN_LEN, SHORT_MAX_LEN, message=CUSTOMID_MESSAGE),
            Regexp(regex=REGEX_CUSTOMID_FORM, message=CUSTOMID_MESSAGE)
        ]
    )
    submit = SubmitField(SUBMIT_BUTTON)

    def validate_custom_id(form, field):
        if URLMap.get_url(short=field.data):
            raise ValidationError(
                EXIST_SHORT_MESSAGE.format(short_name=field.data)
            )
