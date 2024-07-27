from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .constants import (
    ACCEPT, BANNED_SYMBOLS_USED, CUSTOM_ID,
    MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH, ORIGINAL_LINK,
    REGEXP_ACCEPTED_SYMBOLS, REQUIRED_FIELD,
    SHORT_ALREADY_EXIST, URLFIELD_ONLY
)
from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            URL(message=URLFIELD_ONLY),
            Length(max=MAX_ORIGINAL_LENGTH)
        ]
    )
    custom_id = URLField(
        CUSTOM_ID,
        validators=[
            Optional(),
            Length(max=MAX_SHORT_LENGTH),
            Regexp(REGEXP_ACCEPTED_SYMBOLS, message=BANNED_SYMBOLS_USED)
        ]
    )
    submit = SubmitField(ACCEPT)

    def validate_custom_id(self, field):
        custom_id = field.data
        if custom_id is None or URLMap.get(custom_id):
            raise ValidationError(SHORT_ALREADY_EXIST)
