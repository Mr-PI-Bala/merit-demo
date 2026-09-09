#!/usr/bin/env node
/** Explicit live identity smoke. Creates one disposable provider subscriber. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const contract = JSON.parse(fs.readFileSync(path.join(root, 'cfg/alpha_trial_consumer.json'), 'utf8').replace(/^\uFEFF/, ''));
const sync = JSON.parse(fs.readFileSync(path.join(root, 'cfg/merit-sync.json'), 'utf8').replace(/^\uFEFF/, ''));
const gatewayPrefix = String(sync.gateway_api_prefix || '/api/gw').replace(/\/$/, '');
const providerBase = process.env.MERIT_PROD_BASE_URL || sync.metered_api_base || contract.provider_base_url;
const base = `${String(providerBase).replace(/\/$/, '')}${gatewayPrefix}/meritsubs`;
const health = await fetch(`${base}/api/v1/health`, { signal: AbortSignal.timeout(25000) });
let healthBody = null;
try { healthBody = await health.json(); } catch { /* preserve status */ }
if (!health.ok) {
  console.error(`ALPHA SESSION BLOCKED: gateway_health HTTP ${health.status} url=${base}/api/v1/health consumer=${sync.consumer_id}`);
  if (healthBody) console.error(JSON.stringify(healthBody));
  console.error('Deploy the provider gateway route before treating registration as an alpha-ready session check.');
  process.exitCode = 1;
  process.exit();
}
const email = `alpha-${Date.now()}@example.com`;
const response = await fetch(`${base}/api/v1/subscribers/onboard/email`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-Merit-Consumer': sync.consumer_id },
  body: JSON.stringify({ email, consumer_id: sync.consumer_id }),
  signal: AbortSignal.timeout(25000),
});
let body = null;
try { body = await response.json(); } catch { /* preserve status */ }
if (!response.ok || !body?.token || body?.subscriber?.consumer_id !== sync.consumer_id) {
  console.error(`ALPHA SESSION FAILED: HTTP ${response.status} consumer=${sync.consumer_id}`);
  if (body) console.error(JSON.stringify(body));
  process.exitCode = 1;
} else {
  console.log(`ALPHA SESSION OK: consumer=${sync.consumer_id} tier=${body.subscriber?.tier || 'unknown'} token=issued`);
}
