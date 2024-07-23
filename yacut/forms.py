from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError
from wtforms.validators import URL, DataRequired

from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Ссылка на страницу',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Поле для ссылки!')]
    )
    custom_id = URLField(
        'Желаемая ссылка',
    )
    submit = SubmitField('Подтвердить')


    def validate_custom_id(self, field):
        if URLMap.query.filter_by(short=field.data).first():
            raise ValidationError('Извините, данная ссылка уже используется')
