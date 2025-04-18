import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

from testing.redirect.redirect import Redirect


class TestRedirect(unittest.TestCase):
    def setUp(self):
        self.test_file_stream = sys.stdout
        # self.test_file_stream = sys.stderr
        self.redirect = Redirect()

    def test_define_type(self):
        """тест на перенаправление другого потока вывода"""
        self.assertIsInstance(sys.stdout, io.IOBase)

    def test_is_empty(self):
        """случаи использования контекстного менеджера без аргументов"""
        self.assertIsNone(self.redirect.stderr)

    # для этой части теста - закомментировать строки основной программы 48-53
    def test_Redirect_stdout(self):
        """Тест Redirect - проверка перенаправления стандартного вывода (stdout)"""

        # для захвата текста, выводимого в стандартный поток вывода (stdout), позволит "перенаправить" вывод
        stdout_mock = io.StringIO()

        # перенаправление вывода stdout
        # redirect_stdout(stdout_mock) > временно перенаправляет stdout на stdout_mock,
        # Redirect(stdout=stdout_mock) > в классе Redirect заполнение stdout=stdout_mock
        with redirect_stdout(stdout_mock), Redirect(stdout=stdout_mock):
            # вызов внутри блока print() запишет данные в stdout_mock (вместо консоли)
            print("Hello stdout.txt")

        # получение захваченного вывода(все записанное,очищенное от лишних пробелов и символов \n начала и конца)
        captured_output = stdout_mock.getvalue().strip()
        # проверка результата полученного вывода и текста записи
        self.assertEqual(captured_output, "Hello stdout.txt")

    # для этой части теста - закомментировать строки основной программы 48-53
    def test_Redirect_stderr(self):
        # для захвата текста вывода ошибок (stderr)
        stderr_mock = io.StringIO()

        # перенаправление вывода и попытка вызвать исключение-перехватывается и выводится в поток ошибок
        with redirect_stderr(stderr_mock), Redirect(stderr=stderr_mock):
            try:
                raise Exception("Hello stderr.txt")
            except Exception as errors:
                print(str(errors), file=sys.stderr)

        # проверка результата
        captured_output = stderr_mock.getvalue().strip()
        self.assertEqual(captured_output, "Hello stderr.txt")

    # собственно тестов вашего "контекстного менеджера" то и нет: надо проверить работу Redirect - напишите тесты,
    #  в которы примените менеджер Redirect (с with), в тестах пишите в оба указанных в менеджере потока данные, а также
    #  в оба стандартных поток (до и после менеджера) - то есть сделайте print и выбросите исключение. Потом проверьте
    #  в наличие соответствующих данных в соответствующих потоках


if __name__ == "__main__":
    # unittest.main()
    with open("test_results.txt", "a") as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)
