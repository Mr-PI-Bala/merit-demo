# Alpha live-tenant evidence — 2026-09-08

- **Consumer repository:** `merit-demo`
- **Live reference consumer ID:** `merit-demo-alpha`
- **Provider:** `https://merit-prod.vercel.app`
- **Store:** `https://meritstore.vercel.app`
- **Release under test:** `0.3.22`

## Provider activation

The provider's public self-serve activation endpoint returned HTTP 200 for
`merit-demo-alpha` with `activated: true`, `created: true`, and eight seeded
free-community offerings. No subscriber or payment record was submitted.

## Registration route

`GET https://merit-prod.vercel.app/store/merit-demo-alpha/register` returned
HTTP 200 without a redirect, and the response contained `merit-demo-alpha`.
The consumer contract now points to this exact path and fails if the provider
returns a guide, unrelated tenant, or login wall instead.

The explicit disposable-flow check `npm run test:alpha-registration:flow`
created a synthetic `@example.com` free registration, received a provider
registration ID, and completed the provider's Square checkout endpoint with
`free: true`, `status: "paid"`, and no payment required. The command is kept
out of the default suite because it creates a provider trial record.

The provider-reserved `merit-demo` slug remains intentionally excluded from
subscriber acceptance; it redirects to the developer commerce guide. The
repository name and live tenant are therefore separate by design.

## Consumer changes

- `cfg/merit-sync.json`, `cfg/alpha_trial_consumer.json`, tenant manifests,
  diagnostics, portal CTAs, and portal publication slugs use the live tenant.
- Browser evidence remains under `merit-demo docs/evidence/` so changing a
  fork's provider ID does not change the repository's evidence location.
- Contract tests derive the consumer ID from configuration and verify that the
  registration path matches it.
