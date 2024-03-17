import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import threading
import socket_serv

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_html_file('index.html')
        elif self.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path(f'.{self.path}').exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        if self.path == '/message':
            data = self.rfile.read(int(self.headers['Content-Length']))
            self.send_to_socket_server('0.0.0.0', 3000, data)
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())
    
    def send_static(self):
        file_type = self.path.split('/')[-1].split('.')[-1]
        self.send_response(200)
        self.send_header('Content-type', file_type)
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_to_socket_server(self, server_ip:str, server_port:int, data:bytes):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (server_ip, server_port))
        client_socket.close()


def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler):
    server_address=('0.0.0.0', 5000)
    http = HTTPServer(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    th1 = threading.Thread(target=run)
    th2 = threading.Thread(target=socket_serv.run_server)
    th1.start()
    th2.start()


