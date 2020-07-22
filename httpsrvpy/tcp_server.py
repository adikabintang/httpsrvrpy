import socket
import httpsrvpy.handler as handler

class MyTCPServer:
    def __init__(self, conn_handler: handler.MyHandler, addr: str = "127.0.0.1",
                 port: int = 8080):
        self.listen_addr = addr
        self.port = port
        self.handler = conn_handler

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.listen_addr, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1500)
                        if not data:
                            break
                        resp = self.handle_data(data)
                        print(resp)
                        self.send_response(conn, resp)

    def handle_data(self, data):
        return self.handler.handle(data)

    def send_response(self, conn, data):
        conn.sendall(data.encode("utf-8"))
