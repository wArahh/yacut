from flask import redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import generate_short_id


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
