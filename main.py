import http_server
import tcp_server

my_server = tcp_server.MyTCPServer(http_server.MyHttpServer(), "127.0.0.1", 9999)
my_server.start()
