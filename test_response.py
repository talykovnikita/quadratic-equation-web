import allure
import requests
import json


class TestSolution:

    url = "http://localhost:8000"
    encoding = "cp1251"

    def parse_response_body(self, response):
        return json.loads(
            response.content.decode(encoding=self.encoding).replace("'", '"')
        )

    @allure.title("GET: Проверка структуры ответа GET")
    def test_get(self):
        response = requests.get(self.url)

        assert response.status_code == 200

        values = response.content.decode(encoding=self.encoding).split(": ")
        assert len(values) >= 2
        assert values[0] == "Команда"

    @allure.title("POST: целое решение и 2 корня")
    def test_post_two_x(self):
        request_body = {
            "a": 1,
            "b": -5,
            "c": 4,
        }
        expected_response = {"x1": 4, "x2": 1}
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 200, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        assert response_json_body == expected_response, "неверное тело ответа"

    @allure.title("POST: одинаковые корни")
    def test_post_one_x(self):
        request_body = {
            "a": 1,
            "b": -2,
            "c": 1,
        }
        expected_response = {"x1": 1, "x2": 1}
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 200, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        assert response_json_body == expected_response, "неверное тело ответа"

    @allure.title("POST: разные корни")
    def test_post_two_x_round(self):
        request_body = {
            "a": 3,
            "b": -14,
            "c": -5,
        }
        expected_response = {"x1": 5, "x2": -0.33}
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 200, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        assert response_json_body == expected_response, "неверное тело ответа"

    @allure.title("POST: дискрименант меньше нуля")
    def test_post_d_lt_zero(self):
        request_body = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 403, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        error_msg = response_json_body.get("error")

        assert (
            error_msg == "уравнение не имеет решений, дискриминант меньше нуля"
        ), "неверное сообщение об ошибке"

    @allure.title("POST: нет параметра a")
    def test_post_no_a(self):
        request_body = {
            "b": 2,
            "c": 3,
        }
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 422, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        error_msg = response_json_body.get("error")

        assert error_msg == "переданы не все параметры", "неверное сообщение об ошибке"

    @allure.title("POST: нет параметра b")
    def test_post_no_b(self):
        request_body = {
            "a": 1,
            "c": 3,
        }
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 422, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        error_msg = response_json_body.get("error")

        assert error_msg == "переданы не все параметры", "неверное сообщение об ошибке"

    @allure.title("POST: нет параметра c")
    def test_post_no_c(self):
        request_body = {
            "a": 1,
            "b": 3,
        }
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 422, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        error_msg = response_json_body.get("error")

        assert error_msg == "переданы не все параметры", "неверное сообщение об ошибке"

    @allure.title("POST: а=0")
    def test_post_a_is_zero(self):
        request_body = {
            "a": 0,
            "b": 2,
            "c": 3,
        }
        response = requests.post(self.url, json=request_body)
        assert response.status_code == 500, "неверный статус код ответа"

        response_json_body = self.parse_response_body(response)
        error_msg = response_json_body.get("error")

        assert (
            error_msg == "произошла ошибка на стороне сервиса"
        ), "неверное сообщение об ошибке"
