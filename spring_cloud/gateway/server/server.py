# -*- coding: utf-8 -*-
# standard library
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.utils.validate import not_none

hostName = "localhost"
serverPort = 8888


class ServerWebExchange:
    def __init__(self, headers, path, server, method, rfile):
        self.__headers = headers
        self.__path = path
        self.__server = server
        self.__rfile = rfile
        self.__method = method
        self.__attributes = {}

    @property
    def path(self):
        return self.__path

    @property
    def headers(self):
        return self.__headers

    @property
    def host(self):
        return self.__server.server_address[0]

    @property
    def port(self):
        return self.__server.server_address[1]

    @property
    def uri(self):
        return f"http://{self.host}:{self.port}"

    @property
    def cookies(self):
        cookies = {}
        value = self.__headers.get("Cookie")
        if value:
            for segment in re.split(";\\s?", value):
                cookie = re.split("\\s?=\\s?", segment)
                cookies[cookie[0]] = cookie[1]
        return cookies

    @property
    def body(self):
        content_len = int(self.__headers.get("Content-Length"))
        return self.__rfile.read(content_len)

    @property
    def method(self):
        return self.__method

    @property
    def attribute(self):
        return self.__attributes

    def get_required_attribute(self, name: str):
        value = self.__attributes[name]
        not_none(value)
        return value


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def handle_(self):
        exchange = ServerWebExchange(self.headers, self.path, self.server, self.command, self.rfile)
        # scip plugin
        from spring_cloud.gateway.handler.handler import DispatcherHandler

        DispatcherHandler().handle(exchange)

    def do_GET(self):
        self.handle_()

    def do_POST(self):
        self.handle_()

    def do_PUT(self):
        self.handle_()

    def do_DELETE(self):
        self.handle_()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), HTTPRequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
