import unittest
from swagger_tester import swagger_test


class SwaggerTest(unittest.TestCase):
    def test_api(self):
        swagger_test(app_url='http://localhost:8080/api/v1')


if __name__ == '__main__':
    unittest.main()
