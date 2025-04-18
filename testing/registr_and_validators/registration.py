"""
Валидация данных в Эндпоинте /registration:
1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import Email, InputRequired, NumberRange

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    """Класс регистрационной формы"""

    email = StringField(
        validators=[
            InputRequired(message="Обязательно заполнить"),
            Email(message="Не верно заполнен email"),
        ]
    )
    phone = IntegerField(
        validators=[
            InputRequired(message="Обязательно заполнить"),
            NumberRange(
                min=1000000000,
                max=9999999999,
                message="Номер должен содержать десять цифр",
            ),
        ]
    )
    name = StringField(validators=[InputRequired(message="Обязательно заполнить")])
    address = StringField(validators=[InputRequired(message="Обязательно заполнить")])
    index = IntegerField(validators=[InputRequired(message="Обязательно заполнить")])
    comment = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    """Метод регистрации формы"""
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
