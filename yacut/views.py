from flask import abort, flash, redirect, render_template, url_for

from settings import DONE_LINK_MESSAGE, INDEX_VIEW
from . import app
from .error_handler import InvalidDataError, ValidationError
from .forms import YacutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    try:
        url_map = URLMap.create(
            original_link=form.original_link.data,
            custom_id=form.custom_id.data,
        )
    except InvalidDataError as error:
        raise ValidationError(error.messge)
    flash(DONE_LINK_MESSAGE)
    return render_template(
        'index.html',
        form=form,
        short_url=url_for(INDEX_VIEW, _external=True) + url_map.short,
    )


@app.route('/<short_url>', methods=['GET'])
def url_view(short_url):
    url_map = URLMap.get(short=short_url)
    if not url_map:
        abort(404)
    return redirect(location=url_map.original)
