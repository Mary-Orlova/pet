"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализован контекстный менеджер, который принимает два IO-объекта (открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера непозиционные, можно перенаправить только stdout или только stderr.
"""

import sys
import traceback
from types import TracebackType
from typing import IO, Literal, Type


class Redirect:
    """Класс контекстного менеджера"""

    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        """Инициализация объектов stdout,stderr и их предыдущие значения"""
        self.stdout = stdout
        self.stderr = stderr
        self.prev_stdout = sys.stdout
        self.prev_stderr = sys.stderr

    def __enter__(self):
        """вход в контекстный менеджер (перенаправление стандартных потоков вывода на указанные)"""
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> Literal[True]:
        """выход из контекстного менеджера"""

        # если произошло исключение, вывод записывается в stderr
        if exc_type:
            self.stderr.write(traceback.format_exc())
        # восстановление потоков до предыдущих
        sys.stdout = self.prev_stdout
        sys.stderr = self.prev_stderr

        # При тестировании на test_Redirect_stdout и test_Redirect_stderr закомментировать
        # или вообще отказаться от этой части
        # если потоки не закрыты -> закрываются
        if not self.stdout.closed:
            self.stdout.close()
        if not self.stderr.closed:
            self.stderr.close()
        # вызов флага true, чтоб убрать исключения
        return True


if __name__ == "__main__":
    # вывод в стандратный поток - консоль
    print("Hello stdout")

    # создание файлов для потоков
    stdout_file = open("stdout.txt", "w")
    stderr_file = open("stderr.txt", "w")

    # перенаправление потоков вывода: Hello stdout.txt в stdout.txt, Hello stderr.txt -> stderr.txt
    with Redirect(stdout=stdout_file, stderr=stderr_file):
        print("Hello stdout.txt")
        # вызов исключения, обрабатывается в классе Redirect __exit__, стек вызова записывает в stderr.txt
        raise Exception("Hello stderr.txt")

    # попытка вывода в консоль
    print("Hello stdout again")
    # попытка вывода в stder.txt
    raise Exception("Hello stderr")
