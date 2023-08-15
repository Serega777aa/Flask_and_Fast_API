# Создать страницу, на которой будет форма для ввода имени
# и электронной почты
# При отправке которой будет создан cookie файл с данными
# пользователя
# Также будет произведено перенаправление на страницу
# приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка "Выйти"
# При нажатии на кнопку будет удален cookie файл с данными
# пользователя и произведено перенаправление на страницу
# ввода имени и электронной почты.
from flask import Flask, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = """
    <form method=post enctype=multipart/form-data>
    <input type="text" placeholder="Введите имя" name="name"><br>
    <input type="text" placeholder="Введите почту" name="email"><br>
    <input type=submit value=Отправить>
    </form>
    """

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response("Setting a cookie")
        response.set_cookie('name', name, max_age=2592000)
        response.set_cookie('email', email, max_age=2592000)
        return redirect(url_for('hello', name=name, email=email))
    return form


@app.route('/hello/<name>-<email>', methods=['POST', 'GET'])
def hello(name, email):
    form = """
        <form method=post enctype=multipart/form-data>
        <input type=submit value=Выйти>
        </form>
        """
    if request.method == 'POST':
        response = make_response("Cookie")
        response.delete_cookie('name')
        response.delete_cookie('email')
        return redirect(url_for('login'))
    return f'Привет, {name}' + form


if __name__ == '__main__':
    app.run(debug=True)
