#!/usr/bin/env node
/** MERIT consumer E2E smoke — PAR CDN, build artifacts, optional live host. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const pins = readJson(path.join(root, 'cfg/par_pins.json'));
const sync = readJson(path.join(root, 'cfg/merit-sync.json'));
const consumerId = sync.consumer_id;
const failures = [];

async function head(url, label) {
  try {
    const res = await fetch(url, { method: 'HEAD', signal: AbortSignal.timeout(20000) });
    if (!res.ok) failures.push(`${label}: HTTP ${res.status} ${url}`);
    else console.log(`OK HEAD ${label}`);
  } catch (e) {
    failures.push(`${label}: ${e.message}`);
  }
}

function requireFile(rel) {
  const p = path.join(root, rel);
  if (!fs.existsSync(p)) failures.push(`missing ${rel}`);
  else console.log(`OK file ${rel}`);
}

console.log(`=== ${consumerId} E2E ===\n`);

requireFile('play/index.html');
requireFile('journal/index.html');
requireFile('cfg/par_pins.json');
requireFile('dist/config.js');

const play = fs.readFileSync(path.join(root, 'play/index.html'), 'utf8');
if (!play.includes('merit-prod.vercel.app/pkg/meritutils/merit_workbench/0.4.0')) {
  failures.push('play/index.html missing merit_workbench@0.4.0 PAR URL');
}
if (!play.includes('Hello, meritutils') || !play.includes('data-provider-ready')) {
  failures.push('play/index.html missing the hosted meritutils Hello World proof');
}

const wb = pins.packages?.merit_workbench?.artifacts;
const jn = pins.packages?.journal?.artifacts;
if (wb?.js?.url) await head(wb.js.url, 'merit_workbench.js');
if (wb?.css?.url) await head(wb.css.url, 'merit_workbench.css');
if (jn?.mjs?.url) await head(jn.mjs.url, 'journal.mjs');
if (jn?.css?.url) await head(jn.css.url, 'journal.css');

const host = process.env.MERIT_CONSUMER_BASE_URL || process.env.MERIT_DEMO_BASE_URL || '';
if (host) {
  const base = host.replace(/\/$/, '');
  for (const route of ['/diag/manifest.json', '/legal.html']) {
    try {
      const res = await fetch(`${base}${route}`, { signal: AbortSignal.timeout(20000) });
      if (!res.ok) failures.push(`live ${route}: ${res.status}`);
      else console.log(`OK live GET ${route}`);
    } catch (e) {
      failures.push(`live ${route}: ${e.message}`);
    }
  }
} else {
  console.log('(skip live host — set MERIT_DEMO_BASE_URL for deployed smoke)');
}

if (failures.length) {
  console.error('\nE2E FAILED:\n' + failures.map((f) => `  - ${f}`).join('\n'));
  process.exit(1);
}
console.log('\nE2E OK');
