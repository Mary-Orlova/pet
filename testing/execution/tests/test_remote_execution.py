import unittest

from testing.execution.remote_execution import app


class TestRunCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["WTF_CSRF_ENABLED"] = False
        cls.app = app.test_client()
        cls.base_url = "/run_code"

    def test_will_raise_when_timeout_reached(self):
        """Провальный тест"""
        with self.assertRaises(ValueError):
            payload = {"code": "from time import sleep;sleep(10)", "timeout": 1}
            self.app.post(self.base_url, data=payload)

    def test_will_validate(self):
        """Тест валидный"""
        payload = {"code": "from time import sleep;sleep(10)", "timeout": 0}
        response = self.app.post(self.base_url, data=payload)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
