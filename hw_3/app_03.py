# * Доработаем задача про студентов
# * Создать базу данных для хранения информации о студентах и их оценках в
# учебном заведении.
# * База данных должна содержать две таблицы: "Студенты" и "Оценки".
# * В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа и email.
# * В таблице "Оценки" должны быть следующие поля: id, id студента, название
# предмета и оценка.
# * Необходимо создать связь между таблицами "Студенты" и "Оценки".
# * Написать функцию-обработчик, которая будет выводить список всех
# студентов с указанием их оценок.

from flask import Flask, render_template
from models_03 import db, Student, Rating
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Homework_3/Task_3/instance/database_task_3.db'
db.init_app(app)


@app.route('/')
def index():
    return "Hi!"


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("fill-db")
def fill_tables():
    students = [
        ["Иван", "Иванов", 13, "ivanov@mail.ru"],
        ["Петр", "Петров", 24, "petrov@mail.ru"],
        ["Сидоров", "Сидр", 11, "sidorov@mail.ru"],
    ]
    for student in students:
        new_student = Student(name=student[0], surname=student[1], group=student[2], email=student[3])
        db.session.add(new_student)
    db.session.commit()

    faculties = ["Physics", "Mathematics", "Electronics"]
    students = Student.query.all()
    for faculty in faculties:
        for student in students:
            new_rating = Rating(student_id=student.id, sub_study=faculty, rating=random.randint(1, 5))
            db.session.add(new_rating)
            db.session.commit()


@app.route("/students/")
def all_students():
    students_all = Student.query.all()

    students = [[student.name, student.surname, student.group, student.email,
                 Rating.query.filter_by(student_id=student.id).all()] for student in students_all]
    context = {
        "title": "Список студентов",
        "students": students,
    }
    return render_template("all_students.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
