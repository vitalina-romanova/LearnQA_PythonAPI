import requests


class TestEx11:

    def test_homework_cookie(self):
        response = requests.post(
            "https://playground.learnqa.ru/api/homework_cookie"
        )
        print(response.cookies)

        expected_cookie = 'hw_value'
        assert response.cookies['HomeWork'] == expected_cookie, \
            f"Response cookie doesn't match expected_cookie. Response cookie: '{response.cookies}'"
