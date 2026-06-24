# merit-demo — design

**consumer_id:** `merit-demo`  
**Host:** `{operator}.vercel.app` (Angle-4 operators use their own Vercel scope)

## Surfaces (L1 §E.1)

| Slug | Role |
|------|------|
| `/`, `/portal/` | Marketing (here.now publishes `portal/` only) |
| `/play/` | merit_workbench PAR `@0.4.x` |
| `/journal/` | journal PAR + API |
| `/ama/` | AMA Q&A + leaderboard |
| `/api/meritsubs/` | Entitlements stub (wire vendor/meritsubs for production OAuth) |
| `/admin/` | MeritAdminGate operator docs |
| `/diag/` | Deploy manifest |

## White-label

`cfg/branding.json` — operator product name, colors, footer **MERIT Powered** (SomaTune shell via `assets/merit-shell.js`).

## Freemium

`cfg/freemium_limits.json` — journal 2/day; AMA 2 ask/vote/response/day; top 25 leaderboard.

Plus: **$10.79/mo** — `cfg/plus_sku.json` + `cfg/meritstore_tenant.json` offerings seed.

## Data

Optional Supabase (`sql/001_merit_demo.sql`). Without Supabase, journal uses local-only fallback in browser.
