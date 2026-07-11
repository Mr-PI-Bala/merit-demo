# merit-demo — usage

**New creators:** start with **[HowToLaunch-Over-Dinner-Tutorial.md](../HowToLaunch-Over-Dinner-Tutorial.md)** (3 steps, lazy accounts).

Full operator checklist: **[OPERATOR_PROVISION.md](OPERATOR_PROVISION.md)**.  
Vault env compose + deploy phases: **merit-private-vault** → `docs/IAR/MERIT_DEMO_PROVISION_PLAN.md`.

## meritutils usage alignment

merit-demo declares its showcase consumer lane in `cfg/meritutils_consumer.json`. Missing promo codes resolve to `MERITAGENT`, and usage attribution reports affiliate code `MERITDEMO`. The hosted provider controls the intro credit budget (default $25) and Square checkout; this public repo does not expose or own billing logic.

## Build

```powershell
npm install
npm run verify
npm run build
```

## Deploy (operator Vercel scope)

```powershell
# from merit-agent-skills
.\merit.ps1 init --path C:\path\to\merit-demo
# edit C:\path\to\merit-demo\.merit_launch.md
.\merit.ps1 apply --path C:\path\to\merit-demo
.\merit.ps1 deploy --path C:\path\to\merit-demo
```

Set `.merit_launch.md` → mandatory values at the top. `merit apply` writes `.env.local`, `cfg/flask_deploy.json`, and `cfg/portals.json`.

## Env (optional Supabase)

`.env.local`:

```
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
MERIT_CONSUMER_ID=merit-demo
```

Run `sql/001_merit_demo.sql` in consumer Supabase project.

## Portal (here.now BYOK)

```powershell
.\merit.ps1 portal --path .
```

## meritsubs / usage boundary

Production handler policy: public `merit-demo` ships no local meritsubs, AMA, journal, leaderboard, DIRT, or other metered utility handlers. The static shell calls production MERIT Vercel mounts via `MERIT_METERED_API_BASE_URL` and `MERITSUBS_PUBLIC_BASE_URL`.

## meritstore

Provision tenant from `cfg/meritstore_tenant.json` after vault integration cert.

Register: `https://meritstore.vercel.app/merit-demo/register`

## Smokes

- `npm run verify` — scaffold files
- `npm run e2e` — PAR CDN HEAD (set `MERIT_DEMO_BASE_URL` for live host)
- external `GET {MERITSUBS_PUBLIC_BASE_URL}/api/v1/health` — provider health
- external `{MERIT_METERED_API_BASE_URL}/api/ama` and `/api/journal` — metered utility APIs
- `/journal/` — save entry (local or Supabase)
- `/ama/` — ask + vote with privacy modes (geo-IP on Vercel)
- `/admin/` — flexible Plus pricing UI
