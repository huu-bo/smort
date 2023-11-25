from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import time

hostname = 'localhost'
port = 8080

last_update = time.time()
TIMEOUT = 2


def get_html(title: str, content: str, head: str = ''):
    with open('base.html', 'r', encoding='utf-8') as file:
        raw = file.read()
    raw = raw.replace('#t#', title, 1)
    raw = raw.replace('#c#', content, 1)
    raw = raw.replace('#h#', head, 1)
    return raw


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        global last_update
        last_update = time.time()
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(get_html('test', 'Hello, World!').encode('utf-8'))
        elif self.path == '/ping':
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f'<h1>404</h1><p>Path <code>{self.path}</code> not found</p>'.encode('utf-8'))


def host(hostname: str, port: int):
    web_server = HTTPServer((hostname, port), Server)
    print("Server started http://%s:%s" % (hostname, port))
    webbrowser.open('http://%s:%s' % (hostname, port), new=0, autoraise=True)

    web_server.timeout = .3
    try:
        while time.time() - TIMEOUT < last_update:
            web_server.handle_request()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    host(hostname, port)
