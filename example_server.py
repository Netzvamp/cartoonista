from http.server import BaseHTTPRequestHandler
from cartoons import Cartoons


class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        cartoon = Cartoons.get_random_cartoon()
        print(cartoon)
        html = f"""<html>
<html>
<head>
<style>
    body {{ 
        text-align: center; 
        font-family: Arial, Helvetica, sans-serif; 
        margin:30px; 
        background: linear-gradient(
        to bottom,  rgba(216,246,255,1) 0%,rgba(255,255,255,0.32) 68%,rgba(255,255,255,0) 100%); }} 
 img {{display: block;
  margin-left: auto;
  margin-right: auto;}}</style>
</head>
<body>
<h2>Enjoy your day &#128516;</h2>
<div id="cartoon"><h1>{cartoon.get("title", "")}</h1><a href="{cartoon["website"]}"><img src="{cartoon["img"]}"></a><b>{cartoon.get("txt", "")}</b><div>&copy; {cartoon["credits"]}</div></div>
</body>
</html>
        """
        self.wfile.write(html.encode('utf-8'))


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
