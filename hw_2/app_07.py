# Создать страницу, на которой будет форма для ввода числа
# и кнопка "Отправить"
# При нажатии на кнопку будет произведено
# перенаправление на страницу с результатом, где будет
# выведено введенное число и его квадрат.
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def square():
    form = """
        <form method=post enctype=multipart/form-data>
        <input type="text" placeholder="Введите чиcло" name="number"><br>
        <input type=submit value=Отправить>
        </form>
    """

    if request.method == 'POST':
        number = request.form.get('number')
        return f'введенное число = {number}  его квадрат² = {int(number) ** 2}'
    return form


if __name__ == '__main__':
    app.run(debug=True)
