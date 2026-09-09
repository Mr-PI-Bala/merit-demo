#!/usr/bin/env node
/**
 * Explicit live-provider smoke for the free registration path.
 *
 * This creates one disposable free registration on the configured alpha tenant.
 * It is intentionally separate from the default test suite and must be run
 * only when a live provider trial record is acceptable.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const contract = JSON.parse(fs.readFileSync(path.join(root, 'cfg/alpha_trial_consumer.json'), 'utf8').replace(/^\uFEFF/, ''));
const consumerId = contract.consumer_id;
const provider = contract.provider_base_url.replace(/\/$/, '');
const stamp = Date.now();
const handle = `alpha-check-${stamp}`;
const email = `${handle}@example.com`;

const registrationResponse = await fetch(`${provider}/api/v1/tenants/${consumerId}/registrations`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    offering_ids: ['free'],
    guardian: {
      consumer_id: consumerId,
      parent_email: email,
      handle,
      subscriber_id: handle,
    },
    students: [{ plan: 'free' }],
    idempotency_key: `${consumerId}-${stamp}`,
  }),
  signal: AbortSignal.timeout(45000),
});
const registration = await registrationResponse.json().catch(() => ({}));
if (!registrationResponse.ok || !registration.registration_id) {
  throw new Error(`free registration failed: HTTP ${registrationResponse.status} ${registration.error || ''}`.trim());
}

const checkoutResponse = await fetch(`${provider}/api/v1/tenants/${consumerId}/checkout/square`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ registration_id: registration.registration_id }),
  signal: AbortSignal.timeout(45000),
});
const checkout = await checkoutResponse.json().catch(() => ({}));
if (!checkoutResponse.ok || checkout.registration_id !== registration.registration_id || checkout.free !== true || checkout.status !== 'paid') {
  throw new Error(`free checkout failed: HTTP ${checkoutResponse.status} ${checkout.error || JSON.stringify(checkout)}`.trim());
}

console.log(`ALPHA REGISTRATION FLOW OK: consumer=${consumerId} free=true checkout=paid registration_id=${registration.registration_id}`);
