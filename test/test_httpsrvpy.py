import unittest
from httpsrvpy import HTTPStatus, http_server


class TestHttpServer(unittest.TestCase):
    get_req_index = b"""GET /index.html HTTP/1.1\r\n\
Host: 127.0.0.1:9999\r\n\
Connection: keep-alive\r\n\
Upgrade-Insecure-Requests: 1\r\n\
User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36\r\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n\
Sec-Fetch-Site: none\r\n\
Sec-Fetch-Mode: navigate\r\n\
Sec-Fetch-User: ?1\r\n\
Sec-Fetch-Dest: document\r\n\
Accept-Encoding: gzip, deflate, br\r\n\
Accept-Language: en-US,en;q=0.9\r\n\
\r\n"""

    get_req_no_file = b"""GET /thisneverexists HTTP/1.1\r\n\
Host: 127.0.0.1:9999\r\n\
Connection: keep-alive\r\n\
Upgrade-Insecure-Requests: 1\r\n\
User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36\r\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n\
Sec-Fetch-Site: none\r\n\
Sec-Fetch-Mode: navigate\r\n\
Sec-Fetch-User: ?1\r\n\
Sec-Fetch-Dest: document\r\n\
Accept-Encoding: gzip, deflate, br\r\n\
Accept-Language: en-US,en;q=0.9\r\n\
\r\n"""

    get_req_index_invalid = b"""GET /index.html HTP/1.1\r\n\
Host: 127.0.0.1:9999\r\n\
Connection: keep-alive\r\n\
Upgrade-Insecure-Requests: 1\r\n\
User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36\r\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n\
Sec-Fetch-Site: none\r\n\
Sec-Fetch-Mode: navigate\r\n\
Sec-Fetch-User: ?1\r\n\
Sec-Fetch-Dest: document\r\n\
Accept-Encoding: gzip, deflate, br\r\n\
Accept-Language: en-US,en;q=0.9\r\n\
\r\n"""

    def __init__(self, *args, **kwargs):
        super(TestHttpServer, self).__init__(*args, **kwargs)
        self.tested_server = http_server.MyHttpServer()

    def test_handle(self):

        response = self.tested_server.handle(self.get_req_index).decode("iso-8859-1")
        status = response.split('\r\n')[0] + "\r\n"
        self.assertEqual(status, HTTPStatus.OK)

        response = self.tested_server.handle(self.get_req_no_file).decode("iso-8859-1")
        status = response.split('\r\n')[0] + "\r\n"
        self.assertEqual(status, HTTPStatus.NOT_FOUND)

        response = self.tested_server.handle(b"").decode("iso-8859-1")
        status = response.split('\r\n')[0] + "\r\n"
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

        response = self.tested_server.handle(b"non http").decode("iso-8859-1")
        status = response.split('\r\n')[0] + "\r\n"
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

        response = self.tested_server.handle(self.get_req_index_invalid).decode("iso-8859-1")
        status = response.split('\r\n')[0] + "\r\n"
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
    
    def test_parse_header(self):
        headers = self.tested_server.parse_header(self.get_req_index)
        expected_headers = {
            "method": "GET",
            "path": "/index.html",
            "http_version": "HTTP/1.1",
            "Host": "127.0.0.1:9999",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        self.assertDictEqual(expected_headers, headers)

if __name__ == "__main__":
    unittest.main()
