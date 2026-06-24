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
];
const missing = required.filter((r) => !fs.existsSync(path.join(root, r)));
const meritsubsHandler =
  fs.existsSync(path.join(root, 'api/meritsubs/index.py')) ||
  fs.existsSync(path.join(root, 'api/meritsubs/index.mjs'));
if (!meritsubsHandler) missing.push('api/meritsubs handler');
if (missing.length) {
  console.error('verify FAILED:', missing.join(', '));
  process.exit(1);
}
console.log('verify OK: merit-demo consumer scaffold');
process.exit(0);
