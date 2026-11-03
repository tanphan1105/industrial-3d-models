#!/usr/bin/env python3
"""
WT3D Diagnostic Server - lắng nghe report từ color-bridge.js
Chạy: python dope_spy_server.py
"""
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

received = []

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        try:
            data = json.loads(body)
            received.append(data)
            print(f"\n{'='*60}")
            print(f"📡 RECEIVED from {data.get('frame','?')} | {data.get('url','')[:80]}")
            print(f"{'='*60}")
            
            # Canvas
            print(f"🖼️  Canvases: {len(data.get('canvases',[]))}")
            for c in data.get('canvases', []):
                print(f"   [{c['index']}] {c['size']} id={c['id']} keys={c['ownKeys']}")
            
            # __dope keys
            dk = data.get('dopeKeys')
            if dk:
                print(f"\n🎉 window.__dope KEYS ({len(dk)}):")
                print(f"   {dk}")
            else:
                print(f"\n❌ window.__dope: NOT FOUND")
            
            # __dope explore - filter relevant
            explore = data.get('dopeExplore', [])
            bg_related = [e for e in explore if any(x in e['path'].lower() for x in 
                ['background','color','clear','scene','environ','sky','look','appear','render','canvas'])]
            if bg_related:
                print(f"\n🎯 BG/Color related in __dope ({len(bg_related)}):")
                for e in bg_related[:30]:
                    if e['type'] == 'fn':
                        print(f"   FUNC  {e['path']}  (args={e.get('args',0)})")
                    elif e['type'] == 'obj':
                        print(f"   OBJ   {e['path']}  keys={e.get('keys',[][:10])}")
                    else:
                        print(f"   VAL   {e['path']} = {e.get('value','')}")
            
            # All __dope methods
            all_fns = [e for e in explore if e['type'] == 'fn' and e['path'].count('.') == 1]
            if all_fns:
                print(f"\n📋 All __dope direct methods ({len(all_fns)}):")
                for e in all_fns:
                    print(f"   {e['path']}({e.get('args',0)} args)")
            
            # Window renderer
            wr = data.get('windowRenderer')
            if wr:
                print(f"\n🔑 Renderer object at window.{wr['globalKey']}:")
                for e in wr.get('explore', [])[:20]:
                    if e['type'] == 'fn':
                        print(f"   FUNC  {e['path']}")
                    else:
                        print(f"   {e['type'].upper()}  {e['path']} = {e.get('value',e.get('keys',''))}")
            
            # Globals with bg/color
            gbg = data.get('allGlobalsWithBgColor', [])
            if gbg:
                print(f"\n🌍 Globals with bg/color methods:")
                for g in gbg[:10]:
                    print(f"   window.{g['key']}: {g['matches']}")
            
            # Save full JSON
            with open('dope_diagnostic.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full JSON saved to dope_diagnostic.json")
            
        except Exception as ex:
            print(f"❌ Parse error: {ex}\n{body[:200]}")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, *args): pass  # Tắt log request spam

print("🚀 WT3D Dope Spy Server running on http://localhost:19999")
print("   Đang chờ diagnostic từ color-bridge.js...")
print("   (Ctrl+C để dừng)\n")
server = HTTPServer(('localhost', 19999), Handler)
server.serve_forever()
