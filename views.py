import sqlalchemy
from flask import render_template, request

from app_setup import app
from db_setup import db
from tables import Student


@app.route('/')
def index():
    content = list()
    students = db.engine.execute('SELECT * FROM student')
    for i in students:
        content.append({
            "student_id": i[1],
            "surname": i[2],
            "name": i[3],
            "patronymic": i[4],
            "age": i[5],
            "faculty": i[6],
            "course": i[7]
        })
    return render_template("students.html", students=content)


@app.route("/add", methods=["post", "get"])
def add():
    messages = []
    student = {}

    if request.method == "POST":
        for name_col in ("student_id", "surname", "name", "patronymic", "faculty", "age", "course"):
            student[name_col] = data if (data := request.form.get(name_col)) else None
        try:
            student["age"] = int(student['age'])
        except (ValueError, TypeError):
            messages.append('Возраст введен некорректно')

        try:
            student["course"] = int(student['course'])
        except (ValueError, TypeError):
            messages.append('Курс введен некорректно')

        if not messages:
            try:
                Student.add(**student)
                student = {}
            except sqlalchemy.exc.IntegrityError:
                messages = ['Введите все необходимые поля корректно']

    return render_template("add.html", messages=messages, form_data=student)
