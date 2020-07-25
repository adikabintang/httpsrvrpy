import selectors
import socket
import types

import httpsrvpy.handler as handler


class MyTCPServer:
    """
    class MyTCPServer is the TCPserver class to handle incoming TCP request.

    Parameters
    ----------
    conn_handler : handler.MyHandler
        The handler class to handle connection, must be inherited from
        handler.MyHandler
    addr : str
        IPv4 address to listen to. Default: 127.0.0.1. Change to 0.0.0.0 if
        the server needs to handle connection from outside the machine.
    port : int
        The port number to listen to.
    """
    def __init__(self, conn_handler: handler.MyHandler, addr: str = "127.0.0.1",
                 port: int = 8080):
        self.listen_addr = addr
        self.port = port
        self.handler = conn_handler
        self.sel = selectors.DefaultSelector()

    def start(self):
        """run start() to run the server"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.listen_addr, self.port))
            sock.listen()
            sock.setblocking(False)
            self.sel.register(sock, selectors.EVENT_READ, data=None)
            try:
                while True:
                    events = self.sel.select(timeout=None)
                    for key, mask in events:
                        if key.data:
                            self.serve_request(key, mask)
                        else:
                            self.accept_conn(key.fileobj)
            except KeyboardInterrupt:
                print("stop the server")

    def serve_request(self, key, mask):
        """handles incoming request"""
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            received_data = sock.recv(1500)
            if received_data:
                data.outb = self.handler.handle(received_data)
            else:
                # connection closed
                self.sel.unregister(sock)
                sock.close()

        if mask & selectors.EVENT_WRITE:
            if data.outb:
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
                if not data.outb:
                    self.sel.unregister(sock)
                    sock.close()

    def accept_conn(self, sock):
        """accepts incoming connection"""
        conn, addr = sock.accept()
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
