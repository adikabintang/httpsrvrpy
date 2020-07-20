import unittest
from httpsrvpy import HTTPContentType, HTTPStatus, http_server

class TestHttpServer(unittest.TestCase):
    get_req_index = """GET /index.html HTTP/1.1
                    Host: 127.0.0.1:9999
                    Connection: keep-alive
                    Upgrade-Insecure-Requests: 1
                    User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                    Sec-Fetch-Site: none
                    Sec-Fetch-Mode: navigate
                    Sec-Fetch-User: ?1
                    Sec-Fetch-Dest: document
                    Accept-Encoding: gzip, deflate, br
                    Accept-Language: en-US,en;q=0.9"""
    
    get_req_no_file = """GET /whatisthisnotexist HTTP/1.1
                    Host: 127.0.0.1:9999
                    Connection: keep-alive
                    Upgrade-Insecure-Requests: 1
                    User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                    Sec-Fetch-Site: none
                    Sec-Fetch-Mode: navigate
                    Sec-Fetch-User: ?1
                    Sec-Fetch-Dest: document
                    Accept-Encoding: gzip, deflate, br
                    Accept-Language: en-US,en;q=0.9"""

    def test_handle(self):
        tested_server = http_server.MyHttpServer()
        
        response = tested_server.handle(self.get_req_index.encode("utf-8"))
        status = response.split('\r\n')[0] + "\r\n"
        self.assertEqual(status, HTTPStatus.OK)

        response = tested_server.handle(self.get_req_no_file.encode("utf-8"))
        status = response.split('\r\n')[0] + "\r\n"
        self.assertEqual(status, HTTPStatus.NOT_FOUND)

if __name__ == "__main__":
    unittest.main()
