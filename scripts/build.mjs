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

function copyTree(src, dest) {
  if (!fs.existsSync(src)) return;
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) copyTree(from, to);
    else copyFile(from, to);
  }
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
const consumerId = sync.consumer_id || 'merit-demo-alpha';
const limits = readJson('cfg/freemium_limits.json') || {};
const plus = readJson('cfg/plus_sku.json') || {};
const pins = readJson('cfg/par_pins.json') || {};
const portals = readJson('cfg/portals.json') || {};
const meteredBase = (env.MERIT_METERED_API_BASE_URL || sync.metered_api_base || 'https://merit-prod.vercel.app').replace(/\/$/, '');

const configBody = `window.MERIT_DEMO_CONFIG = ${JSON.stringify(
  {
    consumer_id: consumerId,
    supabaseUrl: url,
    supabaseAnonKey: anon,
    branding,
    freemium: limits.guest_and_free || {},
    plusSku: plus.default || {},
    meritstoreRegisterUrl: sync.meritstore_register_url || '',
    meteredApiBase: meteredBase,
    meritsubsBase: env.MERITSUBS_PUBLIC_BASE_URL || sync.meritsubs_base || 'https://merit-prod.vercel.app/api/meritsubs',
    portalUrl: portals.here_now_url || portals.portal_url || '/portal/',
    parPins: pins,
    expectedWorkbenchVersion: pins?.packages?.merit_workbench?.version || '0.4.14',
    healthUrl: `${meteredBase}/api/health`,
  },
  null,
  2
)};\n`;

// Root copy enables the MERIT-managed local HTTP preview; dist is for Vercel.
fs.writeFileSync(path.join(root, 'config.js'), configBody);
fs.writeFileSync(path.join(dist, 'config.js'), configBody);

copyFile(path.join(root, 'assets', 'merit-shell.js'), path.join(dist, 'assets', 'merit-shell.js'));
copyFile(path.join(root, 'assets', 'merit-api.js'), path.join(dist, 'assets', 'merit-api.js'));
copyFile(path.join(root, 'assets', 'consumer.css'), path.join(dist, 'assets', 'consumer.css'));
if (fs.existsSync(path.join(root, 'assets', 'merit-surface.css'))) {
  copyFile(path.join(root, 'assets', 'merit-surface.css'), path.join(dist, 'assets', 'merit-surface.css'));
}

const portalIndex = path.join(root, 'portal', 'index.html');
copyTree(path.join(root, 'portal'), path.join(dist, 'portal'));
// The same portal folder is independently published at a site root (here.now)
// and served at both / and /portal/ on Vercel. Keep root assets available so
// one checked portal artifact works in all three placements.
copyTree(path.join(root, 'portal'), dist);
copyFile(portalIndex, path.join(dist, 'index.html'));

for (const slug of ['play', 'journal', 'ama', 'admin', 'diag']) {
  const src = path.join(root, slug, 'index.html');
  if (fs.existsSync(src)) copyFile(src, path.join(dist, slug, 'index.html'));
}

if (fs.existsSync(path.join(root, 'portal', 'legal.html'))) {
  copyFile(path.join(root, 'portal', 'legal.html'), path.join(dist, 'legal.html'));
}
if (fs.existsSync(path.join(root, 'portal', 'terms.html'))) {
  copyFile(path.join(root, 'portal', 'terms.html'), path.join(dist, 'legal', 'terms.html'));
}

const diag = {
  consumer: consumerId,
  version,
  builtAt: new Date().toISOString(),
  surfaces: ['/', '/play/', '/journal/', '/ama/', '/admin/', '/diag/'],
  supabaseConfigured: !!(url && anon),
  parPins: pins?.packages ? Object.keys(pins.packages) : [],
};
fs.mkdirSync(path.join(dist, 'diag'), { recursive: true });
fs.writeFileSync(path.join(dist, 'diag', 'manifest.json'), `${JSON.stringify(diag, null, 2)}\n`);

console.log(`Built dist/ for ${consumerId}`, version);
console.log('  Supabase:', url ? 'configured' : '(optional — set in .env.local for cloud AMA/journal)');
