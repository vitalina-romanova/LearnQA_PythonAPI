import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User editing cases")
class TestUserEdit(BaseCase):
    def setup(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_data["email"]
        self.password = register_data["password"]
        self.firstName = register_data["firstName"]
        self.user_id = self.get_json_value(response1, "id")

        self.login_data = {
            "email": self.email,
            "password": self.password
        }

        response2 = MyRequests.post("/user/login", data=self.login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @allure.tag("Positive test")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test successfully edits just created user")
    def test_edit_just_created_user(self):

        new_name = 'Changed name'

        response1 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response1, 200)

        response2 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_status_code(response2, 200)

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            new_name,
            f"Wrong firstName of user after edit"
        )

    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test tries to edit user without providing auth data")
    def test_edit_user_wo_auth(self):
        # edit user without providing auth data
        response = MyRequests.put(
            f"/user/{self.user_id}",
            data={"firstName": "new name"}
        )

        Assertions.assert_status_code(response, 400)

        assert response.content.decode(
            "utf-8") == 'Auth token not supplied', f"Unexpected response content = {response.content}"

    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test tries to edit one user while authorized as another")
    def test_edit_user_with_wrong_auth(self):
        # edit user id=2 with auth data from newly created

        new_name = 'Changed name'

        response1 = MyRequests.put(
            f"/user/2",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response1, 200)

        # get user id=2 data
        response2 = MyRequests.get(
            f"/user/2"
        )

        Assertions.assert_json_value_by_name(
            response2,
            "username",
            "Vitaliy",
            f"Username changed, but it shouldn't"
        )

    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test tries to change email to not valid value")
    def test_change_email_not_valid(self):
        new_email = 'email_without_at.example.com'

        response = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, 'Invalid email format')

    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test tries to change name to not valid value")
    def test_change_name_not_valid(self):
        new_name = 'q'

        response = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, '{"error":"Too short value for field firstName"}')
