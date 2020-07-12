from time import gmtime, strftime, ctime
import os.path
from handler import MyHandler


class MyHttpServer(MyHandler):
    def __init__(self):
        self.method = ""
        self.version = ""
        self.path = ""
        self.SERVER_NAME = "MyHttpServer"

    def handle(self, raw):
        payload = raw.decode("utf-8")
        first_line = payload.split('\r\n')[0].split()
        if not first_line[2].startswith("HTTP"):
            return self.prepare_response(400, "text/html")

        self.version = first_line[2][len("HTTP/"):]
        if first_line[0] != "GET":
            return self.prepare_response(405, "text/html",
                                             "This server only serves HTTP GET")

        self.method = first_line[0]
        self.path = first_line[1]
        return self.handle_GET()

    def handle_GET(self):
        file_path = self.path.lstrip("/")
        if not os.path.exists(file_path):
            resp = self.prepare_response(404, "text/html", "file not found")
            return resp

        with open(file_path, "r") as f:
            try:
                content_file = f.read()
                last_modified = strftime("%a, %d %b %Y %H:%M:%S +0000",
                                         gmtime(os.path.getmtime("index.html")))
                resp = self.prepare_response(200, "text/html", content_file,
                                                 last_modified)
                return resp
            except Exception as err:
                pass  # return 503

    def prepare_response(self, status: int, content_type: str,
                             payload: str = "", last_modified: str = "") -> str:

        resp = ""
        http_header = ("Server: {}\r\n"
                       "Date: {}\r\n"
                       "Content-type: {}\r\n"
                       "Content-Length: {}\r\n"
                       "Last-Modified: {}\r\n\r\n").format(
            self.SERVER_NAME,
            strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            content_type, len(payload), last_modified)

        if status == 200:
            http_header = "HTTP/1.0 200 OK\r\n" + http_header
        elif status == 404:
            http_header = "HTTP/1.0 404 File not found\r\n" + http_header
        elif status == 400:
            http_header = "HTTP/1.1 400 Bad Request\r\n" + http_header
        elif status == 405:
            http_header = "HTTP/1.1 405 Method Not Allowed\r\n" + http_header

        resp = http_header + payload
        return resp
