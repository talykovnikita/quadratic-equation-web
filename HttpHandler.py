from http.server import BaseHTTPRequestHandler
import json


class HttpGetHandler(BaseHTTPRequestHandler):

    charset = "cp1251"

    """Обработчик GET запросов"""
    def do_GET(self):
        self._send_text_response(201, "Привет, мир!")

    """Обработчик POST запросов"""
    def do_POST(self):
        input_params = self._parse_input_body()

        self._send_json_response(200, {"a": input_params[0],
                                                                "b": input_params[1],
                                                                "c": input_params[2]})

    """Вспомогательный метод для парсинга тела запросов"""
    def _parse_input_body(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        print(f"Получен запрос с параметрами: {data}")

        return data.get('a'), data.get('b'), data.get('c')

    """Вспомогательный метод для отправки ответа в виде строки"""
    def _send_text_response(self, status_code, response_body):
        # Установка статус кода ответа
        self.send_response(status_code)

        # Установка заголовков
        self.send_header("Content-type", "text/plain")
        self.send_header("charset", self.charset)

        # Добавляет пустую строку после заголовков - требование стандарта http
        self.end_headers()

        # Установка тела ответа
        self.wfile.write(response_body.encode(self.charset))

    """Вспомогательный метод для отправки ответа в виде JSON"""
    def _send_json_response(self, status_code, response_body):
        self.send_response(status_code)
        self.send_header("Content-type", "text/json")
        self.send_header("charset", self.charset)
        self.end_headers()
        self.wfile.write(str(response_body).encode(encoding=self.charset))



