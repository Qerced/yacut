from flask import abort, flash, redirect, render_template, url_for

from settings import URL_VIEW
from . import app
from .error_handler import InvalidDataError
from .forms import YacutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                URL_VIEW,
                _external=True,
                short_url=URLMap.create(
                    original_link=form.original_link.data,
                    short=form.custom_id.data,
                ).short)
        )
    except InvalidDataError as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<short_url>', methods=['GET'])
def url_view(short_url):
    url_map = URLMap.get(short=short_url)
    if not url_map:
        abort(404)
    return redirect(location=url_map.original)
