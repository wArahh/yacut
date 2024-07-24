from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError
from wtforms.validators import URL, DataRequired, Length

from .models import URLMap
from .utils import ACCEPTED_SYMBOLS

short_id_already_exist = 'Предложенный вариант короткой ссылки уже существует.'
banned_symbols_used = 'Нельзя использовать запрещенные символы'


class URLForm(FlaskForm):
    original_link = URLField(
        'Ссылка на страницу',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Поле для ссылки!')]
    )
    custom_id = URLField(
        'Желаемая ссылка',
        validators=[
            Length(
                0, 16,

            )
        ]
    )
    submit = SubmitField('Подтвердить')

    def validate_custom_id(self, field):
        custom_id = field.data
        if custom_id is None:
            return
        if URLMap.query.filter_by(short=custom_id).first():
            raise ValidationError(short_id_already_exist)
        elif any(char not in set(ACCEPTED_SYMBOLS) for char in custom_id):
            raise ValidationError(banned_symbols_used)
