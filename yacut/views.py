from flask import flash, redirect, render_template, request

from . import app, db
from .forms import URLCutForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLCutForm()
    if form.validate_on_submit():
        url = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data or get_unique_short_id()
        )
        db.session.add(url)
        db.session.commit()

        flash(request.host_url + url.short)

    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def forward_view(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)
