import requests


class TestEx12:

    def test_homework_header(self):
        response = requests.post(
            "https://playground.learnqa.ru/api/homework_header"
        )
        print(response.headers)
        excepted_header = "Some secret value"

        assert response.headers['x-secret-homework-header'] == excepted_header, \
            f"Response header doesn't match expected_header. Response header {response.headers}"
