#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sync = JSON.parse(fs.readFileSync(path.join(root, 'cfg/merit-sync.json'), 'utf8').replace(/^\uFEFF/, ''));
const journal = fs.readFileSync(path.join(root, 'journal/index.html'), 'utf8');
const ama = fs.readFileSync(path.join(root, 'ama/index.html'), 'utf8');
const api = fs.readFileSync(path.join(root, 'assets/merit-api.js'), 'utf8');
const session = fs.readFileSync(path.join(root, 'assets/merit-session.js'), 'utf8');
const failures = [];

if (!/^[a-z0-9][a-z0-9-]*$/.test(sync.consumer_id)) failures.push(`consumer_id must be URL-safe, got ${sync.consumer_id}`);
const providerContract = JSON.parse(fs.readFileSync(path.join(root, 'cfg/alpha_trial_consumer.json'), 'utf8').replace(/^\uFEFF/, ''));
if (providerContract.consumer_id !== sync.consumer_id) failures.push('alpha trial contract must match cfg/merit-sync.json consumer_id');
if (!providerContract.expected_register_path.endsWith(`/${sync.consumer_id}/register`)) failures.push('alpha trial contract must target the configured consumer registration path');
for (const [name, page] of [['journal', journal], ['ama', ama]]) {
  if (!page.includes('/assets/merit-api.js')) failures.push(`${name}: missing public API helper`);
  if (!page.includes('window.MERIT_API.request')) failures.push(`${name}: does not use public API helper`);
}
if (!api.includes("'X-Merit-Consumer'")) failures.push('API helper: missing X-Merit-Consumer context');
if (!api.includes("credentials: 'include'")) failures.push('API helper: missing browser credentials');
if (!api.includes("rail('meritsubs', `api/v1/subscribers/onboard/${route}`)")) failures.push('API helper: missing public meritsubs onboarding route');
if (!api.includes('sessionStorage')) failures.push('API helper: session token must be sessionStorage-scoped');
if (!api.includes('function rail(')) failures.push('API helper: missing metered gateway rail builder');
if (!session.includes('merit-session-ready')) failures.push('Session bridge: missing ready event');
if (!session.includes('Open hosted registration')) failures.push('Session bridge: missing hosted registration link');
if (session.includes('localStorage')) failures.push('Session bridge: must not persist bearer tokens in localStorage');
if (/li\.innerHTML\s*=/.test(ama)) failures.push('AMA: API data still assigned to li.innerHTML');
if (!ama.includes('textContent = who') || !ama.includes('textContent = String(question.body || \'\')')) {
  failures.push('AMA: safe text rendering contract missing');
}

if (failures.length) {
  console.error(`ALPHA CONTRACT FAILED\n${failures.map((item) => `- ${item}`).join('\n')}`);
  process.exit(1);
}
console.log(`ALPHA CONTRACT OK: consumer=${sync.consumer_id}, identity context, credentials, safe AMA rendering`);
