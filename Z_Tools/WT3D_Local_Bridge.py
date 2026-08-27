import os, sys, subprocess, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 58921

class BridgeHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/open':
            params = urllib.parse.parse_qs(parsed.query)
            target = params.get('path', [''])[0].strip()
            
            # Xử lý lặp 06_Renders_and_Media nếu có
            if r'06_Renders_and_Media\06_Renders_and_Media' in target:
                target = target.replace(r'06_Renders_and_Media\06_Renders_and_Media', '06_Renders_and_Media')

            target = os.path.normpath(target)
            
            # Tìm thư mục tồn tại gần nhất nếu thư mục con chưa có
            check_path = target
            while check_path and not os.path.exists(check_path):
                parent = os.path.dirname(check_path)
                if parent == check_path:
                    break
                check_path = parent

            if check_path and os.path.exists(check_path):
                try:
                    # Gọi explorer mở cửa sổ thật
                    subprocess.Popen(f'explorer.exe "{check_path}"', shell=True)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(f'{{"status": "ok", "opened": "{check_path.replace(chr(92), "/")}"}}'.encode('utf-8'))
                    return
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(f'{{"status": "error", "message": "{str(e)}"}}'.encode('utf-8'))
                    return

            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status": "not_found"}')
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'{"status": "ready"}')

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), BridgeHandler)
    print(f'[WT3D Bridge] Server running on http://127.0.0.1:{PORT}')
    server.serve_forever()
