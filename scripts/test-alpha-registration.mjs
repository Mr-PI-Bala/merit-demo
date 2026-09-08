#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const contract = JSON.parse(fs.readFileSync(path.join(root, 'cfg/alpha_trial_consumer.json'), 'utf8').replace(/^\uFEFF/, ''));
const failures = [];

try {
  const health = await fetch(contract.health_url, { signal: AbortSignal.timeout(20000) });
  if (!health.ok) failures.push(`provider health: HTTP ${health.status}`);
  else console.log(`OK provider health: ${contract.provider_base_url}`);
} catch (error) {
  failures.push(`provider health: ${error.message}`);
}

try {
  const response = await fetch(contract.register_url, { redirect: 'follow', signal: AbortSignal.timeout(20000) });
  const finalPath = new URL(response.url).pathname.replace(/\/$/, '');
  if (!response.ok) failures.push(`registration: HTTP ${response.status}`);
  if (finalPath !== contract.expected_register_path) {
    failures.push(`registration redirected to ${response.url}; expected ${contract.expected_register_path}`);
  } else {
    console.log(`OK registration route: ${response.url}`);
  }
} catch (error) {
  failures.push(`registration: ${error.message}`);
}

if (failures.length) {
  console.error(`MERIT-DEMO PROVIDER CONTRACT FAILED\n${failures.map((item) => `- ${item}`).join('\n')}`);
  process.exit(1);
}
console.log(`MERIT-DEMO PROVIDER CONTRACT OK: consumer_id=${contract.consumer_id}`);
