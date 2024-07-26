from flask import redirect, render_template, url_for

from . import app
from .constants import DB_ERROR
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def assigning_link_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    try:
        return render_template(
            "index.html",
            form=form,
            short=url_for(
                "redirect_to_url",
                short=URLMap.create_object(
                    form.original_link.data, form.custom_id.data
                ).short,
                _external=True
            ),
        )
    except Exception as error:
        raise DB_ERROR.format(error=error)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url(short):
    return redirect(
        URLMap.get_object(short).first_or_404().original
    )
