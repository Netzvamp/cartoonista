from http.server import BaseHTTPRequestHandler
from cartoons import Cartoons


class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        cartoon = Cartoons.get_random_cartoon()
        if cartoon.get("txt", ""):
            cartoon["txt"] = cartoon["txt"] + "<br>"
        html = f"""<html>
<!doctype html>
<html lang="en">
<head>
<style>
    body {{ 
        text-align: center; 
        font-family: "Comic Sans MS", cursive, sans-serif; 
        background: linear-gradient(
        to bottom,  rgba(216,246,255,1) 0%,rgba(255,255,255,0.32) 68%,rgba(255,255,255,0) 100%); }} 
    .enjoy {{position: absolute; left: 15px; top: 40px;z-index:200; transform: rotate(-30deg);}}
    .cartoon {{ 
        margin-left: auto; margin-right: auto;
        max-height: 100vh; 
}}
    .txt {{ font-weight: bold; margin: 10px; padding: 10px; border: 2px dotted #afafaf; background: #ffffff}}
    img {{background: #ffffff; max-height: 78vh; min-height: 40vh}}
</style>
</head>
<body>
<div class="enjoy"><h2>Enjoy your day &#128516;</h2></div>
<div class="cartoon">
<div><h1>{cartoon.get("title", "")}</h1></div>
<div class="image"><img id="image" src="{cartoon["img"]}" onclick="document.getElementById('image').style.maxHeight='none'"></div>
<div class="txt">{cartoon.get("txt", "")}<a href="{cartoon["website"]}">&copy; {cartoon["credits"]}</a></div></div>
</body>
</html>
        """
        self.wfile.write(html.encode('utf-8'))


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
