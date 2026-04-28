from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired, Length


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
