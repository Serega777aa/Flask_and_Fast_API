from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired, Regexp


class RegistrationForm(FlaskForm):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
    #     message = """Поле пароль должно содержать не менее 8 символов,
    # включая хотя бы одну цифру и одну букву в верхнем и нижнем регистре."""

    name = StringField('Имя', validators=[DataRequired(), Length(min=4, max=30)])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(min=4, max=30)])
    # email = StringField('Email', validators=[DataRequired(), Email(message='Не правильный почтовый адрес!')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # password = PasswordField('Пароль', validators=[InputRequired(), Regexp(regex=pattern, message=message)])
    password = PasswordField('Пароль', validators=[InputRequired(), Regexp(regex=pattern)])
    # confirm_password = PasswordField('Подтвердите пароль', validators=[InputRequired(),
    #                                 EqualTo('password', message='Пароли должны совпадать!')])
    confirm_password = PasswordField('Подтвердите пароль', validators=[InputRequired(), EqualTo('password')])
    date_birth = DateField('Дата рождения', format='%Y-%m-%d')
    personal_data = BooleanField('Согласие на обработку персональных данных', validators=[InputRequired()])
