class HTTPStatus:
    OK = "HTTP/1.0 200 OK\r\n"
    NOT_FOUND = "HTTP/1.0 404 not found\r\n"
    BAD_REQUEST = "HTTP/1.1 400 Bad Request\r\n"
    METHOD_NOT_ALLOWED = "HTTP/1.1 405 Method Not Allowed\r\n"
    INTERNAL_SERVER_ERROR = "HTTP/1.1 500 Internal Server Error\r\n"

class HTTPContentType:
    TEXT_HTML = "text/html"
    JSON = "application/json"

class HTTPMethod:
    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"
    ALL_METHODS = {GET, POST, HEAD, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH}
