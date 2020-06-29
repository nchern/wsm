import threading

from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)


server_address = ('', 65001)


def serve_http(handler=BaseHTTPRequestHandler):
    httpd = HTTPServer(server_address, handler)

    httpd_thread = threading.Thread(target=httpd.serve_forever)
    httpd_thread.setDaemon(True)
    httpd_thread.start()
