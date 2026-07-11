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
