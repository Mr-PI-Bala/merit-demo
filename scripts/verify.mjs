#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = [
  'vercel.json',
  'package.json',
  'cfg/merit-sync.json',
  'cfg/branding.json',
  'cfg/freemium_limits.json',
  'play/index.html',
  'journal/index.html',
  'ama/index.html',
  'portal/legal.html',
  'portal/terms.html',
  'THIRD_PARTY_NOTICES.md',
  'sql/002_ama_daily_activity.sql',
  '.env.local.example',
  'cfg/meritsubs_consumer.json',
  'assets/consumer.css',
  'portal/css/portal.css',
  'portal/js/portal.js',
  'portal/portal.json',
  'scripts/test-fork-contract.mjs',
];
const missing = required.filter((r) => !fs.existsSync(path.join(root, r)));
const forbiddenMeteredHandlers = [
  'api/meritsubs/index.py',
  'api/meritsubs/index.mjs',
  'api/ama/index.mjs',
  'api/journal/index.mjs',
].filter((r) => fs.existsSync(path.join(root, r)));
if (forbiddenMeteredHandlers.length) {
  missing.push(`remove public metered handlers: ${forbiddenMeteredHandlers.join(', ')}`);
}
if (missing.length) {
  console.error('verify FAILED:', missing.join(', '));
  process.exit(1);
}
const checks = [
  ['portal/index.html', '/config.js', 'portal must load runtime config'],
  ['portal/index.html', '/css/portal.css', 'portal must use a root-compatible deployed stylesheet'],
  ['portal/index.html', '/js/portal.js', 'portal must use a root-compatible deployed script'],
  ['journal/index.html', 'Local demo', 'journal must explain its local fallback'],
  ['ama/index.html', 'Local demo mode', 'AMA must explain its local fallback'],
];
const builtFiles = ['dist/css/portal.css', 'dist/js/portal.js', 'dist/portal.json', 'dist/portal/css/portal.css', 'dist/portal/js/portal.js'];
for (const rel of builtFiles) {
  if (!fs.existsSync(path.join(root, rel))) missing.push(`build output missing ${rel}`);
}
if (missing.length) {
  console.error('verify FAILED:', missing.join(', '));
  process.exit(1);
}
for (const [rel, needle, message] of checks) {
  const source = fs.readFileSync(path.join(root, rel), 'utf8');
  if (!source.includes(needle)) {
    console.error(`verify FAILED: ${message}`);
    process.exit(1);
  }
}
console.log('verify OK: merit-demo consumer scaffold');
process.exit(0);
