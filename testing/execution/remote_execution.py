"""
Эндпоинт /run_code принимает на вход код (строка).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

import subprocess

import psutil
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)


class CodeForm(FlaskForm):
    """Класс формы кода
    code:str валидация
    timeout: int заданное время для реализации кода"""

    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[NumberRange(min=1, max=30)])


def run_python_code_in_subproccess(code: str, timeout: int):
    """Запуск кода субпроцесс с использованием psutil"""

    proc = psutil.Popen(
        ["/usr/bin/python3", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    try:
        outs, errs = proc.communicate(timeout=timeout)
        if proc.returncode == 0:
            return outs
        else:
            return errs
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        return f'Исполнение кода "{code}" не уложилось за {timeout} сек.\n{errs}'


@app.route("/run_code", methods=["POST"])
def run_code():
    """Метод запуска кода с эндпойнтом"""
    form = CodeForm()

    if form.validate_on_submit():
        return run_python_code_in_subproccess(form.code.data, form.timeout.data), 200

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
