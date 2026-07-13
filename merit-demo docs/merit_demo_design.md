# merit-demo — design

**consumer_id:** `merit-demo`  
**Host:** `{operator}.vercel.app` (Angle-4 operators use their own Vercel scope)

## Surfaces (L1 §E.1)

| Slug | Role |
|------|------|
| `/`, `/portal/` | Marketing (here.now publishes `portal/` only) |
| `/play/` | merit_workbench PAR `@0.4.x` |
| `/journal/` | journal PAR UI; metered API is production provider mount |
| `/ama/` | AMA UI; metered Q&A/leaderboard API is production provider mount |
| Metered utility APIs | external production MERIT Vercel mounts; no local meritsubs/AMA/journal source in public repo |
| `/api/admin/pricing` | Operator flexible Plus pricing (Supabase `operator_pricing`) |
| `/admin/` | MeritAdminGate + pricing UI |
| `/diag/` | Deploy manifest |

## White-label

`cfg/branding.json` — operator product name, colors, footer **MERIT Powered** (SomaTune shell via `assets/merit-shell.js`).

## Freemium

`cfg/freemium_limits.json` — journal 2/day; AMA 2 ask/vote/response/day; top 25 leaderboard.

Plus: **$10.79/mo** — `cfg/plus_sku.json` + `cfg/meritstore_tenant.json` offerings seed.

## Data

Optional Supabase: `sql/001_merit_demo.sql`, `sql/002_ama_daily_activity.sql`, meritsubs migration on same project. See `OPERATOR_PROVISION.md`.

## Validation lifecycle

`merit-demo` documents and supports `merit.ps1` / `merit.sh` as the public command surface.

| Command | Purpose |
|---|---|
| `./merit.ps1 verify` | Build and verify scaffold, forbidden local metered handlers, and git whitespace |
| `./merit.ps1 e2e` | Run PAR/provider smoke plus Playwright route validation and screenshots |
| `./merit.ps1 deploy` | Verify, link Vercel when missing, deploy production |
| `./merit.ps1 closeout` | Verify, e2e, whitespace, git status/head evidence |

Raw `npm run verify`, `npm run e2e`, `git diff --check`, and `npx vercel` are implementation details under the wrapper.

## Provider-consumer decision

| Edge | Decision | Evidence |
|---|---|---|
| `meritutils → merit-demo` | **ACCEPT** | `merit_workbench@0.4.0` and `journal@0.2.2` load from the canonical production gateway; Playwright validates the visible Hello World proof and hosted registry. |
| `meritsubs → merit-demo` | **ACCEPT** | External production mount only; `https://merit-prod.vercel.app/api/meritsubs/api/v1/health` passes. No provider source is embedded. |
| `meritstore → merit-demo` | **ACCEPT** | Tenant route `https://merit-prod.vercel.app/store/merit-demo/register` is provisioned and returns 200. |

This acceptance covers the public reference-consumer contract. It does not promote the hosted providers beyond their independently declared release stages.
