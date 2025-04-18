"""
Unit-тесты для каждого поля и валидатора в эндпоинте /registration,
проверяет корректность работы валидатора.
Проверка на существование наборов данных, которые проходят и не проходят валидацию.
"""

import unittest

from registration import app


class RegistrationTest(unittest.TestCase):
    """Тест формы регистрации"""

    def setUp(self) -> None:
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.url = "/registration"
        self.app = app.test_client()

        # тестируемые корректные данные формы
        self.correct_data = {
            "email": "tom@google.com",
            "phone": 9999999999,
            "name": "Tom",
            "address": "Moscow",
            "index": 111111,
            "comment": "...",
        }

    def test_can_get_valid_data(self):
        """тест на валидные данные"""
        data = self.correct_data.copy()
        response = self.app.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_can_null_data(self):
        """тест на отсутствие данных, переданных в форму"""
        response = self.app.post(self.url, data={})
        self.assertEqual(response.status_code, 400)

    def test_can_wrong_email(self):
        """тест на не верно указанную почту"""
        data = self.correct_data.copy()
        data["email"] = "test_google.com"
        response = self.app.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("email" in response.text)

    def test_can_get_wrong_phone(self):
        """тест на не верно указанный телефон"""
        data = self.correct_data.copy()
        data["phone"] = "999999"
        response = self.app.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("phone" in response.text)

    def test_can_get_wrong_name(self):
        """тест на не верно указанное имя"""
        data = self.correct_data.copy()
        data["name"] = "test2"
        response = self.app.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("name" in response.text)

    def test_can_get_wrong_address(self):
        """тест на не верный адресс"""
        data = self.correct_data.copy()
        data["address"] = "Test"
        response = self.app.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("address" in response.text)

    def test_can_get_wrong_index(self):
        """тест на не верный индекс"""
        data = self.correct_data.copy()
        data["index"] = "00000"
        response = self.app.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("index" in response.text)

    def test_can_get_wrong_comment(self):
        """тест на не верный комментарий"""
        data = self.correct_data.copy()
        data["comment"] = "same text"
        response = self.app.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("comment" in response.text)


if __name__ == "__main__":
    unittest.main()
