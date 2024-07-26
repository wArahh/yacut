from flask import flash, redirect, render_template, url_for

from . import app
from .constants import URL_SHORT_ERROR, URL_SUCCESSFULLY_SHORTED
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def assigning_link_view():
    form = URLForm()
    if form.validate_on_submit():
        try:
            flash(
                URL_SUCCESSFULLY_SHORTED
            )
            return render_template(
                'index.html',
                form=form,
                short_link=url_for(
                    'redirect_to_url',
                    short=URLMap.create(
                        form.original_link.data, form.custom_id.data
                    ).short, _external=True
                )
            )
        except Exception as error:
            flash(URL_SHORT_ERROR.format(error=error))
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url(short):
    return redirect(
        URLMap.get_object_or_404(short).original
    )
