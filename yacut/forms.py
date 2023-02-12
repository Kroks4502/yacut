from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional,
                                ValidationError, url)

from settings import SHORT_URL_USER_MAX_LEN

from .utils import is_not_uniq_short, is_not_valid_short_id


class URLCutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(), Length(max=512), url()]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=SHORT_URL_USER_MAX_LEN), Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        custom_id = field.data
        if is_not_uniq_short(custom_id):
            raise ValidationError(f'Имя {custom_id} уже занято!')

        if is_not_valid_short_id(custom_id):
            raise ValidationError(
                'Указано недопустимое имя для короткой ссылки')
