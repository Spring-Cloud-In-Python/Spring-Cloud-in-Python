# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from http.server import HTTPServer, SimpleHTTPRequestHandler

# scip plugin
from spring_cloud.gateway.handler import DispatcherHandler
from spring_cloud.gateway.server import DefaultServerHttpRequest, DefaultServerWebExchange, ServerHTTPResponse
from spring_cloud.gateway.server.server import HttpResponseHandler

dispatcher_handler = DispatcherHandler()


class HTTPRequestHandler(SimpleHTTPRequestHandler, HttpResponseHandler):
    def send_body(self, body: bytes):
        self.wfile.write(body)

    def send_status_code(self, status_code: int):
        self.send_response(status_code)

    def handle_(self):
        http_request = DefaultServerHttpRequest(self.headers, self.path, self.server, self.command, self.rfile)
        http_response = ServerHTTPResponse(self)
        exchange = DefaultServerWebExchange(http_request, http_response)
        dispatcher_handler.handle(exchange)

    def do_GET(self):
        self.handle_()

    def do_POST(self):
        self.handle_()

    def do_PUT(self):
        self.handle_()

    def do_PATCH(self):
        self.handle_()

    def do_DELETE(self):
        self.handle_()

    def de_COPY(self):
        self.handle_()

    def do_HEAD(self):
        self.handle_()

    def do_OPTIONS(self):
        self.handle_()

    def de_LINK(self):
        self.handle_()

    def de_UNLINK(self):
        self.handle_()

    def de_LOCK(self):
        self.handle_()

    def de_UNLOCK(self):
        self.handle_()

    def de_PROPFIND(self):
        self.handle_()

    def de_VIEW(self):
        self.handle_()


if __name__ == "__main__":

    hostName = "localhost"
    serverPort = 8888

    webServer = HTTPServer((hostName, serverPort), HTTPRequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
