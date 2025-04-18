"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from types import TracebackType
from typing import Collection, Literal, Type


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        """Инициализация errors"""
        self.errors = tuple(errors)

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        #         exc_type: Type[BaseException] | None,
        #         exc_val: BaseException | None,
        #         exc_tb: TracebackType | None
        # ) -> Literal[True] | None:
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> Literal[True]:
        # Если исключение в self.errors-возвращает True(обработка исключения и игнорирование),
        # Иначе возвращаем None(ошибка прокидывается выше по стеку)
        # if issubclass(exc_type, self.errors):
        #     return True
        # return None
        if exc_type not in self.errors and not any(
            issubclass(exc_type, i) for i in self.errors
        ):
            return False
        else:
            return True


err_types = {BaseException}

with BlockErrors(err_types):
    a = 1 / 0
print("Выполнено без ошибок")
