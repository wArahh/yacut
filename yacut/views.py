from flask import flash, redirect, render_template, url_for

from . import app
from .constants import (
    REDIRECT_URL, UNEXPECTED_NAME, URL_ALREADY_EXISTS, DB_ERROR
)
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def assigning_link_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_link=url_for(
                REDIRECT_URL,
                short=URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data,
                    unexpected_name_error=ValueError(UNEXPECTED_NAME),
                    url_already_exists_error=ValueError(URL_ALREADY_EXISTS),
                ).short, _external=True
            )
        )
    except ValueError as error:
        flash(DB_ERROR.format(error=error))
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url(short):
    return redirect(
        URLMap.get_or_404(short).original
    )
