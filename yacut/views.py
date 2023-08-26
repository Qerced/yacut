from flask import abort, flash, redirect, render_template, url_for

from settings import DONE_LINK_MESSAGE, INDEX_VIEW

from . import app
from .forms import YacutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    if not form.custom_id.data:
        form.custom_id.data = URLMap.get_unique_short_id(
            form.original_link.data
        )
    urlmap = URLMap.create(
        original_link=form.original_link.data,
        custom_id=form.custom_id.data,
    )
    flash(DONE_LINK_MESSAGE)
    return render_template(
        'index.html',
        form=form,
        short_url=url_for(INDEX_VIEW, _external=True) + urlmap.short,
    )


@app.route('/<short_url>', methods=['GET'])
def url_view(short_url):
    url = URLMap.get(short=short_url)
    if not url:
        abort(404)
    return redirect(location=url.original)
