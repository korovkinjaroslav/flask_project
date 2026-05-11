from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, SubmitField, BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('Текст поста', validators=[DataRequired(), Length(min=1, max=8000)])
    image = FileField('Картинка (можно не прикладывать)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только jpg, png'),
    ])
    submit = SubmitField('Опубликовать')
