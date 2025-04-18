"""
Собственный аналог встроенному валидатору NumberRange для ограничения числа по его длине - для поля phone.
Валидатор принимает на вход параметры min и max — мин. и макс. длина,а так же опциональный параметр message.
Реализован двумя способами.
"""

from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    """Метод валидации поля phone"""

    def _number_length(form: FlaskForm, field: Field):
        # если кол-во символов номера меньше мин. или больше макс.кол-ва разряда ожидаемого числа - выдать ошибку
        # тут "длина" это разрядность числа (количество цифр, пример: у номера телефона без учтета 8 или +7 ровно
        #  10 разрядов), согласитесь, работать с таким валидатором намного удобнее, чем указывать сами значения числа
        if len(str(field.data)) < min or len(str(field.data)) > max:
            raise ValidationError()

    return _number_length


class NumberLength:
    """Класс номера телефона"""

    def __init__(self, min: int, max: int, message: Optional[str] = None):
        """Инициация макс и мин кол-ва цифр поля phone + сообщение"""
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        """Метод call для валидации поля phone"""
        if len(str(field.data)) < self.min or len(str(field.data)) > self.max:
            raise ValidationError()
