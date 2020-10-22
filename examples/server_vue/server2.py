from http.server import ThreadingHTTPServer
from http.server import BaseHTTPRequestHandler
import webbrowser
from urllib import parse
from string import Template
import json
from cartoonista import Cartoons


class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            'command={}'.format(self.command),
            'path={}'.format(self.path),
            'real path={}'.format(parsed_path.path),
            'query={}'.format(parsed_path.query),
            'request_version={}'.format(self.request_version),
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version),
            'sys_version={}'.format(self.sys_version),
            'protocol_version={}'.format(self.protocol_version),
            '',
            'HEADERS RECEIVED:',
        ]
        print(message_parts)
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            cartoon = Cartoons.get_random_cartoon()
            if cartoon.get("txt", ""):
                cartoon["txt"] = cartoon["txt"] + "<br>"
                
            with open("cartoon.html") as f:
                html = Template(f.read())
                html = html.safe_substitute(
                    img=cartoon['img'],
                    website=cartoon['website'],
                    credits=cartoon['credits'],
                    title=cartoon.get("title", ""),
                    txt=cartoon.get("txt", "")
                )
                self.wfile.write(html.encode('utf-8'))
        elif self.path == "/cartoon.css":
            with open("cartoon.css") as f:
                self.send_response(200)
                self.send_header('Content-Type', 'text/css; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
        elif self.path == "/cartoon.js":
            with open("cartoon.js") as f:
                self.send_response(200)
                self.send_header('Content-Type', 'text/javascript; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
        elif self.path == "/rest/cartoons/include":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            output = json.dumps(Cartoons.get_all_cartoonists())
            self.wfile.write(output.encode('utf-8'))
        elif self.path == "/rest/cartoons/cartoon":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            output = json.dumps(Cartoons.get_random_cartoon())
            self.wfile.write(output.encode('utf-8'))
        else:
            self.send_error(404, message="Not found")


if __name__ == '__main__':
    server = ThreadingHTTPServer(('localhost', 8080), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    webbrowser.open('http://127.0.0.1:8080')
    server.serve_forever()
