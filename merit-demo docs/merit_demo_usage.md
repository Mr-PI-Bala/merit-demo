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

Production handler: `api/meritsubs/index.mjs` relays to hosted MERIT services. Provider billing, usage metering, and Square logic are not embedded in this public repo.

## meritstore

Provision tenant from `cfg/meritstore_tenant.json` after vault integration cert.

Register: `https://meritstore.vercel.app/merit-demo/register`

## Smokes

- `npm run verify` — scaffold files
- `npm run e2e` — PAR CDN HEAD (set `MERIT_DEMO_BASE_URL` for live host)
- `GET /api/meritsubs` — health
- `GET /api/meritsubs/api/v1/entitlements` — guest tier
- `/journal/` — save entry (local or Supabase)
- `/ama/` — ask + vote with privacy modes (geo-IP on Vercel)
- `/admin/` — flexible Plus pricing UI
