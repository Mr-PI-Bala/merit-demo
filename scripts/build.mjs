#!/usr/bin/env node
/** Build dist/ for Vercel — MERIT L1 §E.1 consumer surfaces. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const dist = path.join(root, 'dist');

function loadEnv(filePath) {
  const env = {};
  if (!fs.existsSync(filePath)) return env;
  for (const line of fs.readFileSync(filePath, 'utf8').split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const i = t.indexOf('=');
    if (i === -1) continue;
    env[t.slice(0, i).trim()] = t.slice(i + 1).trim().replace(/^["']|["']$/g, '');
  }
  return env;
}

function copyFile(src, dest) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

function readJson(rel) {
  const p = path.join(root, rel);
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
}

const env = loadEnv(path.join(root, '.env.local'));
const url = env.SUPABASE_URL || env.NEXT_PUBLIC_SUPABASE_URL || '';
const anon = env.SUPABASE_ANON_KEY || env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const version = fs.existsSync(path.join(root, 'VERSION'))
  ? fs.readFileSync(path.join(root, 'VERSION'), 'utf8').trim()
  : '0.3.0';

fs.mkdirSync(dist, { recursive: true });

const branding = readJson('cfg/branding.json') || {};
const sync = readJson('cfg/merit-sync.json') || {};
const limits = readJson('cfg/freemium_limits.json') || {};
const plus = readJson('cfg/plus_sku.json') || {};

fs.writeFileSync(
  path.join(dist, 'config.js'),
  `window.MERIT_DEMO_CONFIG = ${JSON.stringify(
    {
      consumer_id: sync.consumer_id || 'merit-demo',
      supabaseUrl: url,
      supabaseAnonKey: anon,
      branding,
      freemium: limits.guest_and_free || {},
      plusSku: plus.default || {},
      meritstoreRegisterUrl: sync.meritstore_register_url || '',
      meritsubsBase: sync.meritsubs_base || '/api/meritsubs',
    },
    null,
    2
  )};\n`
);

copyFile(path.join(root, 'assets', 'merit-shell.js'), path.join(dist, 'assets', 'merit-shell.js'));

const portalIndex = path.join(root, 'portal', 'index.html');
copyFile(portalIndex, path.join(dist, 'index.html'));
copyFile(portalIndex, path.join(dist, 'portal', 'index.html'));

for (const slug of ['play', 'journal', 'ama', 'admin', 'diag']) {
  const src = path.join(root, slug, 'index.html');
  if (fs.existsSync(src)) copyFile(src, path.join(dist, slug, 'index.html'));
}

if (fs.existsSync(path.join(root, 'portal', 'legal.html'))) {
  copyFile(path.join(root, 'portal', 'legal.html'), path.join(dist, 'legal.html'));
}

const pins = readJson('cfg/par_pins.json');
const diag = {
  consumer: sync.consumer_id || 'merit-demo',
  version,
  builtAt: new Date().toISOString(),
  surfaces: ['/', '/play/', '/journal/', '/ama/', '/api/meritsubs/', '/admin/', '/diag/'],
  supabaseConfigured: !!(url && anon),
  parPins: pins?.packages ? Object.keys(pins.packages) : [],
};
fs.mkdirSync(path.join(dist, 'diag'), { recursive: true });
fs.writeFileSync(path.join(dist, 'diag', 'manifest.json'), `${JSON.stringify(diag, null, 2)}\n`);

console.log('Built dist/ for merit-demo', version);
console.log('  Supabase:', url ? 'configured' : '(optional — set in .env.local for cloud AMA/journal)');
