"""
This module contains HTTP server implementation (class MyHttpServer) and
custom exception for the HTTP server (class MyHttpServerError)
"""
import datetime
import logging
import mimetypes
import os.path
from time import gmtime, strftime
from httpsrvpy import HTTPMethod, HTTPStatus
from httpsrvpy.handler import MyHandler


class MyHttpServer(MyHandler):
    """
    class MyHttpServer is a class that is inherited from MyHandler to provide
    an HTTP server capability on top of class MyTCPServer.

    This class overrides the handle(raw) function. Currently, it only supports
    HTTP GET request. A custom HTTP handler class can also be created by deriving
    from this class. For example, a class MyCustomHTTPServer(MyHttpServer) can
    override handle_get(path) to handle request and to do other things such as
    reading from database or something else and return a json string.
    """
    SERVER_NAME = "MyHttpServer"

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def handle(self, raw) -> str:
        """
        Defines what to do upon receiving a request from a client.

        Parameters
        ----------
        raw : bytearray
            The data sent by the client.
        """
        try:
            logging.debug(raw)
            headers = self.parse_header(raw)
            logging.debug(headers)
            if headers["method"] == HTTPMethod.GET:
                return self.handle_GET(headers["path"])

            return self.prepare_response(HTTPStatus.METHOD_NOT_ALLOWED,
                                         "This server only serves HTTP GET")
        except MyHttpServerError as err:
            return self.prepare_response(HTTPStatus.BAD_REQUEST, err.message)

    @staticmethod
    def parse_header(raw) -> dict:
        """
        Parses HTTP headers and return the header as a dictionary.

        Parameters
        ----------
        raw : bytearray
            The data sent by the client.

        Returns
        -------
        dict
            Dictionary of HTTP headers
        """
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

    def handle_GET(self, path: str):
        """
        Handles HTTP GET request from a client.

        Parameters
        ----------
        path : str
            The URL of the requested resource

        Returns
        -------
        bytearray
            The HTTP response (header + payload)
        """
        file_path = path.lstrip("/")
        if not os.path.exists(file_path):
            return self.prepare_response(HTTPStatus.NOT_FOUND, "file not found")

        with open(file_path, "rb") as f:
            current_time = datetime.datetime.now()
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

                logging.info("%s,,%s", current_time, HTTPStatus.OK)
                return self.prepare_response(HTTPStatus.OK,
                                             content_file, more_headers)
            except OSError as err:
                logging.error("%s,OS error: %s,%s", current_time, err,
                              HTTPStatus.INTERNAL_SERVER_ERROR)
                return self.prepare_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                             f"OS error: {err}")
            except BaseException as err:
                logging.error("%s,error reading files: %s,%s", current_time, err,
                              HTTPStatus.INTERNAL_SERVER_ERROR)
                return self.prepare_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                             f"error reading files: {err}")

    def prepare_response(self, status, payload, more_headers: dict = None):
        """
        Prepares HTTP response: headers + payload.

        Parameters
        ----------
        status : str
            The HTTP status, see HTTPStatus
        payload : bytearray or string
            The HTTP body
        more_headers : dict
            More user-defined HTTP headers

        Returns
        -------
        bytearray
            The HTTP response (header + payload), iso-8859-1 encoded
        """
        http_header = status + f"Server: {self.SERVER_NAME}\r\n" + \
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime())}\r\n" + \
            f"Content-Length: {len(payload)}\r\n" + \
            "Connection: close\r\n"

        if more_headers:
            for key, value in more_headers.items():
                http_header += f"{key}: {value}\r\n"

        if isinstance(payload, str):
            http_header += "Content-type: text/html\r\n"
            payload = payload.encode("iso-8859-1")

        http_header += "\r\n"

        return http_header.encode("iso-8859-1") + payload


class MyHttpServerError(Exception):
    """
    Custom exception raised when incoming HTTP header is invalid.
    """
    def __init__(self, message="invalid http header"):
        self.message = message
