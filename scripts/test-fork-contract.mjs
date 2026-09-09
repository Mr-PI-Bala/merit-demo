#!/usr/bin/env node
/** Check that the reference app's identity and brand are fork configuration, not route code. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (rel) => fs.readFileSync(path.join(root, rel), 'utf8');
const sync = JSON.parse(read('cfg/merit-sync.json').replace(/^\uFEFF/, ''));
const branding = JSON.parse(read('cfg/branding.json').replace(/^\uFEFF/, ''));
const generated = read('config.js');
const failures = [];

if (!sync.consumer_id || !/^[a-z0-9][a-z0-9-]*$/.test(sync.consumer_id)) {
  failures.push('cfg/merit-sync.json must provide a URL-safe consumer_id');
}
if (!generated.includes(`"consumer_id": "${sync.consumer_id}"`)) {
  failures.push('generated config.js does not carry cfg/merit-sync.json consumer_id');
}
if (!generated.includes(String(branding.product_name))) {
  failures.push('generated config.js does not carry cfg/branding.json product_name');
}
const ama = read('ama/index.html');
const registrationFlow = read('scripts/test-alpha-registration-flow.mjs');
if (!ama.includes("cfg.consumer_id || 'merit-demo-alpha'")) failures.push('AMA local storage must use generated consumer_id');
if (registrationFlow.includes('merit-demo-alpha')) failures.push('registration flow smoke must derive its idempotency key from configured consumer_id');
const portal = read('portal/js/portal.js');
if (!portal.includes('runtimeBrand') || !portal.includes('runtime.meritstoreRegisterUrl')) {
  failures.push('portal must derive brand and registration links from generated runtime config');
}
for (const rel of ['portal/ama/index.html', 'portal/journal/index.html', 'portal/subs/index.html']) {
  if (!read(rel).includes('/css/portal.css')) failures.push(`${rel} must use the shared portal stylesheet`);
}
for (const rel of ['portal/ama/index.html', 'portal/journal/index.html', 'portal/subs/index.html']) {
  if (/https:\/\/merit-demo\.vercel\.app/i.test(read(rel))) failures.push(`${rel} must not hardcode the reference deployment URL`);
}
for (const rel of ['portal/index.html', 'portal/ama/index.html', 'portal/journal/index.html', 'portal/subs/index.html']) {
  if (read(rel).includes('/portal/')) failures.push(`${rel} must use root-compatible links for independent portal publication`);
}

if (failures.length) {
  console.error(`FORK CONTRACT FAILED\n${failures.map((failure) => `- ${failure}`).join('\n')}`);
  process.exit(1);
}
console.log(`FORK CONTRACT OK: consumer_id=${sync.consumer_id}, brand=${branding.product_name}`);
