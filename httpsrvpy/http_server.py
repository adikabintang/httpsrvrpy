from time import gmtime, strftime
from httpsrvpy.handler import MyHandler
from httpsrvpy import HTTPStatus, HTTPContentType, HTTPMethod
import os.path

class MyHttpServer(MyHandler):
    SERVER_NAME = "MyHttpServer"

    def handle(self, raw) -> str:
        try:
            headers = self.parse_header(raw)
            if headers["method"] == HTTPMethod.GET:
                return self.handle_GET(headers["path"])

            return self.prepare_response(HTTPStatus.METHOD_NOT_ALLOWED,
                                         HTTPContentType.TEXT_HTML,
                                         "This server only serves HTTP GET")
        except MyHttpServerError as err:
            return self.prepare_response(
                HTTPStatus.BAD_REQUEST, HTTPContentType.TEXT_HTML, err.message)

    def parse_header(self, raw: str) -> dict:
        if not raw:
            raise MyHttpServerError()

        payload = raw.decode("utf-8")
        header = payload.split('\r\n\r\n')[0]
        if not header:
            raise MyHttpServerError()

        http_header_attr = dict()
        all_lines = header.split('\r\n')
        first_line = all_lines[0]
        if not first_line:
            raise MyHttpServerError()

        first_line_splitted = first_line.split()
        if len(first_line_splitted) != 3 or \
                not first_line_splitted[2].startswith("HTTP") or \
                not first_line_splitted[1].startswith("/") or \
                first_line_splitted[0] not in HTTPMethod.ALL_METHODS:
            raise MyHttpServerError()

        http_header_attr["method"] = first_line_splitted[0]
        http_header_attr["path"] = first_line_splitted[1]
        http_header_attr["http_version"] = first_line_splitted[2]
        if len(all_lines) > 1:
            for line in all_lines[1:]:
                splitted = line.split(": ")
                if len(splitted) != 2:
                    raise MyHttpServerError()

                http_header_attr[splitted[0]] = splitted[1]

        return http_header_attr

    def handle_GET(self, path: str) -> str:
        file_path = path.lstrip("/")
        if not os.path.exists(file_path):
            return self.prepare_response(HTTPStatus.NOT_FOUND,
                                         HTTPContentType.TEXT_HTML,
                                         "file not found")

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                content_file = f.read()
                last_modified = strftime("%a, %d %b %Y %H:%M:%S +0000",
                                         gmtime(os.path.getmtime(file_path)))
                return self.prepare_response(HTTPStatus.OK,
                                             HTTPContentType.TEXT_HTML,
                                             content_file, last_modified)
            except OSError as err:
                return self.prepare_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                             HTTPContentType.TEXT_HTML,
                                             f"OS error: {err}")
            except BaseException as err:
                return self.prepare_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                             HTTPContentType.TEXT_HTML,
                                             f"error when reading files: {err}")

    def prepare_response(self, status, content_type: str,
                         payload: str = "", last_modified: str = "",
                         additional_headers: dict = None) -> str:

        http_header = status + f"Server: {self.SERVER_NAME}\r\n" + \
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime())}\r\n" + \
            f"Content-type: {content_type}\r\n" + \
            f"Content-Length: {len(payload)}\r\n"

        if last_modified:
            http_header += "Last-Modified: " + last_modified + "\r\n"

        if additional_headers:
            for key, value in additional_headers.items():
                http_header += f"{key}: {value}\r\n"

        return http_header + "\r\n" + payload


class MyHttpServerError(Exception):
    def __init__(self, message="invalid http header"):
        self.message = message
