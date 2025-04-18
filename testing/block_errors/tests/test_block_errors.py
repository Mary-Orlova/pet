import unittest

from testing.block_errors.block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_will_ignore_errors(self):
        """Тест, где ошибка игнорируется"""
        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            a = 1 / 0
        print("Выполнено без ошибок")

    def test_will_up_errors(self):
        """Тест, где ошибка прокидывается выше"""
        err_types = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / "0"
            print("Выполнено без ошибок")

    def test_will_up_inside_irnoge_out(self):
        """Тест, где ошибка прокидывается выше во внутреннем блоке и игнорируется во внешнем"""
        outer_err_types = {TypeError}
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with BlockErrors(inner_err_types):
                a = 1 / "0"
            print("Внутренний блок: выполнено без ошибок")
        print("Внешний блок: выполнено без ошибок")

    def test_will_irnote_children_errors(self):
        """Тест, где дочерние ошибки игнорируются"""
        err_types = {Exception}
        with BlockErrors(err_types):
            a = 1 / "0"
        print("Выполнено без ошибок")


if __name__ == "__main__":
    unittest.main()
