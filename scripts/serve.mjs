import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const portIndex = args.indexOf('--port');
const port = Number(portIndex >= 0 ? args[portIndex + 1] : 3000);
const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.ico': 'image/x-icon'
};

function safePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split('?')[0]);
  const candidate = path.resolve(root, `.${decoded === '/' ? '/index.html' : decoded}`);
  return candidate.startsWith(root + path.sep) ? candidate : null;
}

const server = http.createServer(async (req, res) => {
  try {
    const requested = safePath(req.url || '/');
    if (!requested) { res.writeHead(400); res.end('Bad path'); return; }
    let target = requested;
    try { await readFile(target); } catch { target = path.join(requested, 'index.html'); }
    const file = await readFile(target);
    res.writeHead(200, {
      'Content-Type': mime[path.extname(target).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-store'
    });
    res.end(file);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('MERIT demo page not found');
  }
});

server.listen(port, () => {
  console.log(`MERIT demo serving ${root}`);
  console.log(`Open http://localhost:${port}/play/`);
});
