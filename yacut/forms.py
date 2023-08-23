from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .validators import UrlExistValidator

ERROR_MESSAGE = 'Имя {short_name} уже занято!'
ERROR_MESSAGE_API = 'Имя "{short_name}" уже занято.'


class YacutForm(FlaskForm):
    def __init__(self, run_from_api=False, *args, **kwargs):
        super(YacutForm, self).__init__(*args, **kwargs)
        self.run_from_api = run_from_api

    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='"url" является обязательным полем!'),
            Length(17, 256), URL(message='Запрещенные символы')
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                1, 16, message='Указано недопустимое имя для короткой ссылки'
            ),
            UrlExistValidator(),
            Regexp(
                regex='[A-Za-z0-9]+$',
                message='Указано недопустимое имя для короткой ссылки'
            )
        ]
    )
    submit = SubmitField("Создать")
