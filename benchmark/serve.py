from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'source'),**kw)
 def do_POST(self):
  if self.path!='/results' or self.headers.get('Origin')!='http://127.0.0.1:8101':self.send_error(403);return
  n=int(self.headers.get('Content-Length','0'))
  if not 0<n<10000000:self.send_error(413);return
  data=json.loads(self.rfile.read(n));p=ROOT/'rerun-results.tmp';p.write_text(json.dumps(data,indent=2));p.replace(ROOT/'rerun-results.json');self.send_response(200);self.end_headers();self.wfile.write(b'OK')
print('http://127.0.0.1:8101',flush=True)
ThreadingHTTPServer(('127.0.0.1',8101),H).serve_forever()
