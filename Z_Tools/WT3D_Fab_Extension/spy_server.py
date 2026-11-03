import json, sys, time
def _save_probe(data):
    if data.get('type') == 'probe':
        with open('probe_full.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
from http.server import HTTPServer, BaseHTTPRequestHandler

ALLOWED_ORIGIN = 'https://www.fab.com'

class Handler(BaseHTTPRequestHandler):
    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'unsafe-none')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        self.send_response(200)
        self._cors_headers()
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

        try:
            body_str = raw.decode('utf-8', errors='replace')
            data = json.loads(body_str)

            t = data.get('type', '?')
            _save_probe(data)
            frame = data.get('frame', '?')
            ts = time.strftime('%H:%M:%S')

            line = f'[{ts}] [{t}] from {frame}: '

            if t == 'spy_xhr':
                line += f"{data.get('method')} {data.get('url')} | body: {data.get('body')}"
            elif t == 'spy_xhr_response':
                line += f"HTTP {data.get('status')} {data.get('url')} | resp: {str(data.get('response'))[:200]}"
            elif t == 'spy_fetch':
                line += f"{data.get('method')} {data.get('url')} | body: {data.get('body')}"
            elif t == 'spy_runAction':
                line += f"ACTION: {data.get('action')} | payload: {data.get('payload')}"
            elif t == 'spy_patchDoptions_native':
                line += f"NATIVE PATCH: uid={data.get('uid')} | patch={json.dumps(data.get('patch'))}"
            elif t == 'spy_user_click':
                line += f"CLICK: <{data.get('tag')}> class='{data.get('className')}' text='{data.get('text')}'"
            elif t == 'spy_user_input':
                line += f"INPUT: <{data.get('tag')} type='{data.get('type')}'> val='{data.get('value')}'"
            elif t == 'spy_bg_changed_in_ram':
                line += f"RAM BG CHANGED: {json.dumps(data.get('current'))}"
            elif t == 'probe':
                line += f"PROBE: sceneUid={data.get('sceneUid')} | bg={json.dumps(data.get('doptionsBg'))}"
            elif t == 'color_applied':
                line += f"COLOR APPLIED: hex={data.get('hex')} | ram={data.get('ramUpdated')} | patchErr={data.get('patchError')}"
            else:
                line += json.dumps(data)[:200]

            sys.stdout.write(line + '\n')
            sys.stdout.flush()

            # Append to persistent log
            with open('spy_events.log', 'a', encoding='utf-8') as f:
                f.write(line + '\n')
                if t in ('spy_xhr', 'spy_patchDoptions_native', 'spy_bg_changed_in_ram', 'probe'):
                    f.write('   FULL: ' + json.dumps(data, ensure_ascii=False) + '\n')

            # Also save last dump
            with open('dope_diag.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as ex:
            sys.stdout.write(f'ERR parsing body: {ex}\n')
            sys.stdout.flush()

    def log_message(self, *args):
        pass

sys.stdout.write('Radar Server running on localhost:19999\n')
sys.stdout.flush()
HTTPServer(('localhost', 19999), Handler).serve_forever()
