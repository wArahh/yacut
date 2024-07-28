from flask import flash, redirect, render_template

from . import app
from .exceptions import (
    DuplicateShortURLError, ShortURLError, TooManyAttemptsError
)
from .forms import URLForm
from .models import URLMap
from .utils import get_short_link


@app.route('/', methods=['GET', 'POST'])
def assigning_link_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_link=get_short_link(
                URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data,
                    validated=True
                ).short
            )
        )
    except (
        ShortURLError,
        DuplicateShortURLError,
        TooManyAttemptsError
    ) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url(short):
    return redirect(
        URLMap.get_or_404(short).original
    )
