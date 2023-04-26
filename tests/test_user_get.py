from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Get user data")
class TestUserGet(BaseCase):

    @allure.tag("Positive test")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test successfully gets user name only without auth")
    def test_get_user_details_no_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    @allure.tag("Positive test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test successfully gets all user data with auth")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.tag("Positive test")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test gets only username of user if requested by another authorized user")
    def test_get_user_details_auth_as_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.get(
            f"/user/1",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_no_key(response2, "email")
        Assertions.assert_json_has_no_key(response2, "firstName")
        Assertions.assert_json_has_no_key(response2, "lastName")
