from httpsrvpy import http_server, tcp_server

my_server = tcp_server.MyTCPServer(http_server.MyHttpServer())
my_server.start()
