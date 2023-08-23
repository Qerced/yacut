from flask import jsonify, request
from werkzeug.datastructures import ImmutableMultiDict

from . import app, db
from .error_handler import InvalidAPIUsage
from .forms import YacutForm
from .models import URLMap
from .utils import get_unique_short_id


_Run_from_api = True


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    form = YacutForm(
        _Run_from_api,
        ImmutableMultiDict(
            {
                'original_link': data.get('url'),
                'custom_id': data.get('custom_id') if data.get('custom_id') else ''
            }
        ),
        meta={'csrf': False}
    )
    if form.validate():
        if 'custom_id' not in data:
            form.custom_id.data = get_unique_short_id(data.get('url'))
        url = URLMap.query.filter_by(short=form.custom_id.data).first()
        if url is None:
            url = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data
            )
            db.session.add(url)
        else:
            url.short = form.custom_id.data
        db.session.commit()
        return jsonify(url.to_dict()), 201
    else:
        raise InvalidAPIUsage(
            *form.original_link.errors,
            *form.custom_id.errors
        )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original})
