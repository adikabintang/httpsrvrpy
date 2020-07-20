from time import gmtime, strftime
import os.path
from httpsrvpy.handler import MyHandler
from httpsrvpy import HTTPStatus, HTTPContentType


class MyHttpServer(MyHandler):
    SERVER_NAME = "MyHttpServer"

    def __init__(self):
        pass

    def handle(self, raw) -> str:
        payload = raw.decode("utf-8")
        first_line = payload.split('\r\n')[0].split()
        if not first_line[2].startswith("HTTP"):
            return self.prepare_response(
                HTTPStatus.BAD_REQUEST, HTTPContentType.TEXT_HTML)

        #http_version = first_line[2][len("HTTP/"):]
        if first_line[0] != "GET":
            return self.prepare_response(HTTPStatus.METHOD_NOT_ALLOWED,
                                         HTTPContentType.TEXT_HTML,
                                         "This server only serves HTTP GET")

        #method = first_line[0]
        path = first_line[1]
        return self.handle_GET(path)

    def handle_GET(self, path: str) -> str:
        file_path = path.lstrip("/")
        if not os.path.exists(file_path):
            return self.prepare_response(HTTPStatus.NOT_FOUND,
                                         HTTPContentType.TEXT_HTML,
                                         "file not found")

        with open(file_path, "r") as f:
            try:
                content_file = f.read()
                last_modified = strftime("%a, %d %b %Y %H:%M:%S +0000",
                                         gmtime(os.path.getmtime(file_path)))
                return self.prepare_response(HTTPStatus.OK,
                                             HTTPContentType.TEXT_HTML,
                                             content_file, last_modified)
            except Exception as err:
                return self.prepare_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                             HTTPContentType.TEXT_HTML, err)

    def prepare_response(self, status, content_type: str,
                         payload: str = "", last_modified: str = "") -> str:

        http_header = status + ("Server: {}\r\n"
                                "Date: {}\r\n"
                                "Content-type: {}\r\n"
                                "Content-Length: {}\r\n").format(
            self.SERVER_NAME,
            strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            content_type, len(payload))

        if len(last_modified) > 0:
            http_header += "Last-Modified: " + last_modified + "\r\n"

        return http_header + "\r\n" + payload
