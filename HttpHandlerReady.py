from http.server import BaseHTTPRequestHandler
import json

from Solution import Solution


class HttpGetHandlerReady(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self._send_text_response(200, "Команда: бабусины гуси")

    """Обработчик POST запросов"""

    def do_POST(self):
        input_body = self._parse_input_body()

        if None in input_body:
            self._send_json_response(
                422, self._make_error_body("переданы не все параметры")
            )
            return

        s = Solution(*input_body)

        d = s.calc_d()
        if d < 0:
            self._send_json_response(
                403,
                self._make_error_body(
                    "уравнение не имеет решений, дискриминант меньше нуля"
                ),
            )
            return

        x1 = None
        try:
            x1 = s.calc_x1()
        except:
            self._send_json_response(
                500, self._make_error_body("произошла ошибка на стороне сервиса")
            )
            return

        x2 = None
        try:
            x2 = s.calc_x2()
        except:
            self._send_json_response(
                500, self._make_error_body("произошла ошибка на стороне сервиса")
            )
            return

        self._send_json_response(200, {"x1": x1, "x2": x2})

    """Вспомогательный метод для парсинга тела запросов"""

    def _parse_input_body(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        print(f"Получен запрос с параметрами: {data}")

        return data.get("a"), data.get("b"), data.get("c")

    """Вспомогательный метод для отправки ответа в виде строки"""

    def _send_text_response(self, status_code, response_body):
        print(f"Response: {status_code} with body: {response_body}")
        # Установка статус кода ответа
        self.send_response(status_code)

        # Установка заголовков
        self.send_header("Content-type", "text/plain")
        self.send_header("charset", "cp1251")

        # Добавляет пустую строку после заголовков - требование стандарта http
        self.end_headers()

        # Установка тела ответа
        self.wfile.write(response_body.encode("cp1251"))

    """Вспомогательный метод для отправки ответа в виде JSON"""

    def _send_json_response(self, status_code, response_body):
        print(f"Response: {status_code} with body: {response_body}")
        self.send_response(status_code)
        self.send_header("Content-type", "text/json")
        self.send_header("charset", "cp1251")
        self.end_headers()
        self.wfile.write(json.dumps(response_body).encode(encoding="cp1251"))

    """Вспомогательный метод для формирования ошибки"""

    def _make_error_body(self, msg):
        return {"error": msg}
