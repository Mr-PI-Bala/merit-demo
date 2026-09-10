# merit-demo SOTU - 2026-09-09

## Current live status — canonical merit-prod plane

**Consumer release:** `v0.3.28`
**Consumer ID:** `merit-demo-alpha`
**Provider:** `https://merit-prod.vercel.app`

| Gate | Current result | Evidence |
|---|---|---|
| Consumer verification | PASS | `npm run verify` passes for the released checkout. |
| Provider health | PASS, HTTP 200 | `GET /api/health` reports the canonical MERIT gateway. |
| Registration | PASS, HTTP 200 | `/store/merit-demo-alpha/register` resolves to the expected page. |
| MeritSubs gateway health | BLOCKED, HTTP 404 | `/api/gw/meritsubs/api/v1/health` is not deployed on canonical production. |
| Member session/onboarding | BLOCKED | The consumer test stops at gateway health and will not claim a session-ready result. |

### Release decision

`merit-demo` is **not subscriber-alpha ready**. The consumer shell and registration edge work, but the canonical provider gateway route is missing. The provider owner must deploy the gateway route, then prove onboarding, token issuance, consumer isolation, and the member browser pathway before alpha invitations.

This SOTU covers only `merit-demo` → `merit-prod.vercel.app`. V01/vMERIT testing belongs to the separate `merit-vdemo` plane and is not a readiness signal for this consumer.

The detailed command output and screenshots are in [ALPHA-2026-09-09.md](evidence/ALPHA-2026-09-09.md).

## Executive status

merit-demo remains the public reference consumer for the meritutils provider lane. The checked-in live tenant is `merit-demo-alpha`; the repository slug `merit-demo` remains reserved by the provider as a showcase alias. **Pass 1 (2026-09-05):** `/play/` DualRail `createAppShell` + pinned `merit_workbench@0.4.14` mount reports **Hosted Ready** (or labeled offline stub). It is still not a billing/entitlement/provider authority.

## 2026-07-11 production metered-mount boundary

Public `merit-demo` no longer ships local metered utility handlers. The local meritsubs relay and local AMA/journal handlers were removed so users cannot modify public source to bypass usage metrics, promo validation, entitlement checks, or Square charging. The static shell now points at production MERIT Vercel mounts through `MERIT_METERED_API_BASE_URL` and `MERITSUBS_PUBLIC_BASE_URL`.

## MERIT utilities usage alignment

Consumer manifest: `cfg/meritutils_consumer.json`.

| Package | Pin | Use |
|---|---:|---|
| `merit_workbench` | `meritutils/merit_workbench@0.4.14` | Shared play/workbench shell |
| `journal` | `meritutils/journal@0.2.2` | Deprecated-compatible legacy journal demo |
| `merit_journal` | `meritutils/merit_journal@0.3.0` | New journal lane |
| `merit_ama` | `meritutils/merit_ama@0.1.0` | AMA question/vote showcase |
| `merit_leaderboard` | `meritutils/merit_leaderboard@0.1.0` | AMA/journal ranking showcase |
| `merit_usage_meter` | `meritutils/merit_usage_meter@0.1.1` | Usage/audit metering |

Default promo is `MERITAGENT`; affiliate code is `MERITDEMO`. M4FI is intentionally excluded from this closeout.

## E2E TDD plan

| Persona | Path | Assertion |
|---|---|---|
| Community member | `/play/` | workbench loads from PAR CDN and routes into demo surfaces |
| AMA participant | AMA showcase | asks/votes call production metered mount with `MERITAGENT` |
| Journal user | journal showcase | UI remains static while metered journal calls go to production provider mount |
| Operator | usage manifest | missing promo resolves to `MERITAGENT`; affiliate remains `MERITDEMO` |

## Closeout note

Provider health, registry, MeritSubs health, and the app-specific registration route pass for `merit-demo-alpha`. The reserved `merit-demo` alias still redirects to the developer commerce guide by provider policy; the consumer contract and fork instructions therefore use the live app tenant and require every fork to provision a distinct slug.
