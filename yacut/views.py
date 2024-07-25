from flask import redirect, render_template, url_for

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def assigning_link_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    short = form.custom_id.data
    if short is None:
        short = URLMap.generate_unique_short_id()
    URLMap.check_and_create(form.original_link.data, short)
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
    print(URLMap.get_object(short_id))
    return redirect(
        URLMap.get_object(short_id).original
    )
