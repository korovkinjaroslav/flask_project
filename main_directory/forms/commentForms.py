from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    content = TextAreaField('Комментарий', validators=[DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField('Отправить')
