from wtforms.validators import ValidationError
from wtforms import URLField

from .models import URLMap

ERROR_MESSAGE = 'Имя {short_name} уже занято!'
ERROR_MESSAGE_API = 'Имя "{short_name}" уже занято.'


class UrlExistValidator(object):
    def __init__(self, message=None):
        if not message:
            message = ERROR_MESSAGE_API
        self.message = message

    def __call__(self, form, field):
        if isinstance(field, URLField):
            field = field.data
        if form:
            if not form.run_from_api:
                self.message = ERROR_MESSAGE

        if URLMap.query.filter_by(short=field).first() is not None:
            raise ValidationError(self.message.format(short_name=field))


def short_validator(field):
    try:
        UrlExistValidator()(form=None, field=field)
    except ValidationError:
        return True
    return False
