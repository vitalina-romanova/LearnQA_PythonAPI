from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import allure
import time


@allure.epic("User deletion cases")
class TestUserDelete(BaseCase):
    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Try to delete user that can't be deleted")
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_status_code(response1, 200)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_text(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.tag("Positive test")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Try to delete just created user")
    def test_delete_created_user(self):
        # create user
        reg_data = self.prepare_registration_data()

        email = reg_data["email"]
        password = reg_data["password"]

        response1 = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        login_data = {
            "email": email,
            "password": password
        }

        # user login
        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)

        # get auth data
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response2, 'user_id')

        # delete user using auth data
        response3 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        Assertions.assert_status_code(response3, 200)

        # try to get user's info
        response4 = MyRequests.get(
            f"/user/{user_id_from_auth_method}"
        )

        Assertions.assert_status_code(response4, 404)
        Assertions.assert_response_text(response4, "User not found")

    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Try to delete user with another user's auth")
    def test_delete_created_user_by_user2(self):
        reg_data1 = self.prepare_registration_data()

        response1_1 = MyRequests.post("/user/", data=reg_data1)

        Assertions.assert_status_code(response1_1, 200)
        Assertions.assert_json_has_key(response1_1, "id")

        new_user_id1 = self.get_json_value(response1_1, 'id')

        time.sleep(1)

        reg_data2 = self.prepare_registration_data()

        response2_1 = MyRequests.post("/user/", data=reg_data2)

        Assertions.assert_status_code(response2_1, 200)
        Assertions.assert_json_has_key(response2_1, "id")

        email2 = reg_data2["email"]
        password2 = reg_data2["password"]

        login_data2 = {
            "email": email2,
            "password": password2
        }

        response2_2 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response2_2, 'auth_sid')
        token2 = self.get_header(response2_2, 'x-csrf-token')

        response3 = MyRequests.delete(
            f"/user/{new_user_id1}",
            headers={'x-csrf-token': token2},
            cookies={'auth_sid': auth_sid2}
        )

        Assertions.assert_status_code(response3, 200)

        response4 = MyRequests.get(f"/user/{new_user_id1}")
        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_has_key(response4, "username")
