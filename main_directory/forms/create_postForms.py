from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('Текст поста', validators=[DataRequired(), Length(min=1, max=8000)])
    image = FileField('Картинка (можно не прикладывать)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только jpg, png'),
    ])
    submit = SubmitField('Опубликовать')
