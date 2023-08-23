from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import YacutForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            form.custom_id.data = get_unique_short_id(
                form.original_link.data
            )
        url = URLMap.query.filter_by(original=form.original_link.data).first()
        if url is None:
            url = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data
            )
            db.session.add(url)
        else:
            url.short = form.custom_id.data
        db.session.commit()
        flash('Ваша новая ссылка готова:')
        return render_template(
            'index.html', form=form, short_url='http://localhost/' + url.short)
    return render_template('index.html', form=form)


@app.route('/<short_url>', methods=['GET', 'POST'])
def url_view(short_url):
    url = URLMap.query.filter_by(short=short_url).first()
    if not url:
        abort(404)
    return redirect(location=url.original)
