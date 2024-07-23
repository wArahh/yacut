import random
import string

from flask import redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


ACCEPTED_SYMBOLS = string.ascii_letters + string.digits


def generate_short_id(length=1):
    short_id = ''.join(random.choice(
        ACCEPTED_SYMBOLS
    ) for _ in range(length))
    while URLMap.query.filter_by(short=short_id).first() is not None:
        short_id = generate_short_id(length+1)
    return short_id


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    short = form.custom_id.data
    if not short:
        short = generate_short_id()
    db.session.add(
        URLMap(
            original=form.original_link.data,
            short=short,
        )
    )
    db.session.commit()
    return render_template(
        "index.html",
        form=form,
        short_link=url_for(
            "redirect_to_url",
            short_id=short,
            _external=True
        ),
    )


@app.route('/<string:short_id>', methods=['GET'])
def redirect_to_url(short_id):
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original
    )
