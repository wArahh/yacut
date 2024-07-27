from flask import flash, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_URL, URL_SHORT_ERROR
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
                    form.original_link.data, form.custom_id.data
                ).short, _external=True
            )
        )
    except URL_SHORT_ERROR:
        flash(URL_SHORT_ERROR)
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url(short):
    return redirect(
        URLMap.get_or_404(short).original
    )
