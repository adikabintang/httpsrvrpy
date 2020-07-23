from time import gmtime, strftime
from httpsrvpy.handler import MyHandler
from httpsrvpy import HTTPStatus, HTTPMethod
import logging
import mimetypes
import os.path


class MyHttpServer(MyHandler):
    SERVER_NAME = "MyHttpServer"

    def handle(self, raw) -> str:
        try:
            headers = self.parse_header(raw)
            if headers["method"] == HTTPMethod.GET:
                return self.handle_GET(headers["path"])

            return self.prepare_response(HTTPStatus.METHOD_NOT_ALLOWED,
                                         "This server only serves HTTP GET")
        except MyHttpServerError as err:
            return self.prepare_response(HTTPStatus.BAD_REQUEST, err.message)

    def parse_header(self, raw) -> dict:
        if not raw:
            raise MyHttpServerError()

        # https://tools.ietf.org/html/rfc7230#section-3.2.4
        # HTTP is encoded with ISO-8859-1
        payload = raw.decode("iso-8859-1")
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
            return self.prepare_response(HTTPStatus.NOT_FOUND, "file not found")

        with open(file_path, "rb") as f:
            try:
                more_headers = dict()
                content_file = f.read()
                more_headers["Last-Modified"] = strftime(
                    "%a, %d %b %Y %H:%M:%S +0000",
                    gmtime(os.path.getmtime(file_path)))

                type_and_encoding = mimetypes.guess_type(file_path)
                more_headers["Content-type"] = type_and_encoding[0]
                if type_and_encoding[1]:
                    more_headers["Content-Encoding"] = type_and_encoding[1]

                return self.prepare_response(HTTPStatus.OK,
                                             content_file, more_headers)
            except OSError as err:
                logging.error("OS error: %s" % err)
                return self.prepare_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                             f"OS error: {err}")
            except BaseException as err:
                logging.error("error reading files: %s" % err)
                return self.prepare_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                             f"error reading files: {err}")

    def prepare_response(self, status, payload, more_headers: dict = None):
        http_header = status + f"Server: {self.SERVER_NAME}\r\n" + \
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime())}\r\n" + \
            f"Content-Length: {len(payload)}\r\n"

        if more_headers:
            for key, value in more_headers.items():
                http_header += f"{key}: {value}\r\n"

        if isinstance(payload, str):
            http_header += "Content-type: text/html\r\n"
            payload = payload.encode("iso-8859-1")

        http_header += "\r\n"

        return http_header.encode("iso-8859-1") + payload


class MyHttpServerError(Exception):
    def __init__(self, message="invalid http header"):
        self.message = message
