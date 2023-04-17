from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_massage):
        try:
            response_as_dict = response.json()
        except json.JSONDecoderError:
            assert False, f"Responce is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Responce JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_massage
