import fs from 'node:fs';
import path from 'node:path';

function authorized(req) {
  const expected = process.env.MERITDEMO_ADMIN_KEY || '';
  const auth = req.headers.authorization || '';
  return Boolean(expected && auth.startsWith('Bearer ') && auth.slice(7) === expected);
}

export default function handler(req, res) {
  if (!authorized(req)) return res.status(401).json({ error: 'admin_auth_required' });
  const html = fs.readFileSync(path.join(process.cwd(), 'api', 'admin', 'ui', 'admin.html'), 'utf8');
  res.setHeader('Cache-Control', 'no-store');
  return res.status(200).send(html);
}
