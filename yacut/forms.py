from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError
from wtforms.validators import URL, DataRequired, Length, Regexp

from .models import URLMap
from settings import ACCEPTED_SYMBOLS
from .constants import (SHORT_ID_ALREADY_EXIST, BANNED_SYMBOLS_USED, ORIGINAL_LINK,
                        CUSTOM_ID, REQUIRED_FIELD, URLFIELD_ONLY, ACCEPT, MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH)


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK,
        validators=[DataRequired(message=REQUIRED_FIELD),
                    URL(message=URLFIELD_ONLY), Length(max=MAX_ORIGINAL_LENGTH)]
    )
    custom_id = URLField(
        CUSTOM_ID,
        validators=[Length(max=MAX_SHORT_LENGTH), Regexp(f'^[{ACCEPTED_SYMBOLS}]*$', message=BANNED_SYMBOLS_USED)]
    )
    submit = SubmitField(ACCEPT)

    def validate_custom_id(self, field):
        custom_id = field.data
        if custom_id is None:
            return
        if URLMap.query.filter_by(short=custom_id).first():
            raise ValidationError(SHORT_ID_ALREADY_EXIST)
