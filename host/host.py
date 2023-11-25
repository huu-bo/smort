from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import time

hostname = 'localhost'
port = 8080

last_update = time.time()
TIMEOUT = 2
html: bytes = b''


def get_html(title: str, content: str, head: str = '', filename: str = 'host/base.html'):
    with open(filename, 'r', encoding='utf-8') as file:
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
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html)
        elif self.path == '/ping':
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f'<h1>404</h1><p>Path <code>{self.path}</code> not found</p>'.encode('utf-8'))

    def log_message(self, format, *args):
        pass


def host(hostname: str, port: int, html_: str):
    web_server = HTTPServer((hostname, port), Server)
    print("Server started http://%s:%s" % (hostname, port))
    webbrowser.open('http://%s:%s' % (hostname, port), new=0, autoraise=True)

    global html
    html = html_.encode('utf-8')

    global last_update
    last_update = time.time()

    web_server.timeout = .3
    try:
        while time.time() - TIMEOUT < last_update:
            web_server.handle_request()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    host(hostname, port, get_html('test', 'Hello, World!', filename='base.html'))
