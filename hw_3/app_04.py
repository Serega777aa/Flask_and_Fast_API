# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля:
# "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных,
# а пароль должен быть зашифрован.
import secrets

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

from forms import RegistrationForm
from models_04 import db, User

secret_key = secrets.token_hex()
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Homework_3/Task_4-8/instance/database_task_4_8.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    # if request.method == 'POST' and form.validate():
    if request.method == 'POST' and form.validate_on_submit():
        # Обработка данных из формы
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        if User.query.filter_by(name=name).first():
            flash('Пользователь с таким именем уже зарегистрирован!')
            return redirect(url_for('registration'))

        elif User.query.filter_by(email=email).first():
            flash('Пользователь с таким E-mail уже зарегистрирован!')
            return redirect(url_for('registration'))
        else:
            password = generate_password_hash(form.password.data)
            date_birth = form.date_birth.data
            user = User(name=name, surname=surname, email=email, password=password, date_birth=date_birth)
            db.session.add(user)
            db.session.commit()
            print(f'Add user {name}!')
            flash('Регистрация выполнена!')
            return redirect(url_for("index"))
    elif request.method == 'POST':
        if form.email.errors:
            flash('Не правильный почтовый адрес!')
            return redirect(url_for("registration"))
        elif form.password.errors:
            flash("""Поле пароль должно содержать не менее 8 символов, 
включая хотя бы одну цифру и одну букву в верхнем и нижнем регистре.""")
            return redirect(url_for("registration"))
        elif form.confirm_password.errors:
            flash('Пароли должны совпадать!')
            return redirect(url_for("registration"))
        elif form.date_birth.errors:
            flash('Выберите дату. Дата не может быть пустой!')
            return redirect(url_for("registration"))
    return render_template('registration.html', form=form)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


if __name__ == '__main__':
    app.run(debug=True)
