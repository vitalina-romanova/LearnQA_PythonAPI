import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    bad_data = [
        ({"password": "123", "username": "learnqa", "firstName": "learanqa", "lastName": "learnqa",
          "email": "wrongemailexample.com"}, ("Invalid email format")),
        ({"username": "learnqa", "firstName": "learanqa", "lastName": "learnqa", "email": "email45example.com"},
         ("The following required params are missed: password")),
        ({"password": "123", "firstName": "learanqa", "lastName": "learnqa", "email": "email45example.com"},
         ("The following required params are missed: username")),
        ({"password": "123", "username": "learnqa", "lastName": "learnqa", "email": "email45example.com"},
         ("The following required params are missed: firstName")),
        ({"password": "123", "username": "learnqa", "firstName": "learanqa", "email": "email45example.com"},
         ("The following required params are missed: lastName")),
        ({"password": "123", "username": "learnqa", "firstName": "learanqa", "lastName": "learnqa"},
         ("The following required params are missed: email")),
        ({"password": "123", "username": "a", "firstName": "learanqa", "lastName": "learnqa",
          "email": "email@45example.com"}, ("The value of 'username' field is too short")),
        ({"password": "123", "username": "b" * 251, "firstName": "learanqa", "lastName": "learnqa",
          "email": "email45@example.com"}, ("The value of 'username' field is too long"))
    ]

    @allure.tag("Positive test")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Succesfully create new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Create new user with same email as existing user")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}"

    @allure.tag("Negative test")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Create new user with wrong input data")
    @pytest.mark.parametrize('bad_data', bad_data)
    def test_create_user_validation_errors(self, bad_data):
        data_set = bad_data[0]

        response = MyRequests.post("/user/", data=data_set)

        Assertions.assert_status_code(response, 400)
        assert response.text == bad_data[1]
