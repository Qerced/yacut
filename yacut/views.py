from flask import abort, redirect, render_template, url_for

from settings import DONE_LINK_MESSAGE

from . import app
from .forms import YacutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        url = URLMap.get_or_create(
            original=form.original_link.data,
            short=form.custom_id.data
        )
        return render_template(
            'index.html',
            form=form,
            short_url=url_for('index_view', _external=True) + url.short,
            flash_messages=DONE_LINK_MESSAGE
        )
    return render_template('index.html', form=form)


@app.route('/<short_url>', methods=['GET'])
def url_view(short_url):
    url = URLMap.get_url(short=short_url)
    if not url:
        abort(404)
    return redirect(location=url.original)
