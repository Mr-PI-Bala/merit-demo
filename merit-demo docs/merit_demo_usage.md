# merit-demo — usage

Full operator checklist: **[OPERATOR_PROVISION.md](OPERATOR_PROVISION.md)**.  
Vault env compose + deploy phases: **merit-private-vault** → `docs/IAR/MERIT_DEMO_PROVISION_PLAN.md`.

## Build

```powershell
npm install
npm run verify
npm run build
```

## Deploy (operator Vercel scope)

```powershell
# from merit-agent-skills
.\merit-live.ps1 deploy vercel --path C:\path\to\merit-demo
```

Set `cfg/flask_deploy.json` → `vercel_scope` to **your** team.

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
.\merit-live.ps1 portal publish --path . --all
```

## meritsubs embed

```powershell
.\scripts\embed-meritsubs.ps1
```

Production handler: `api/meritsubs/index.py` + `vendor/meritsubs/` (replaces Node stub).

## meritstore

Provision tenant from `cfg/meritstore_tenant.json` after vault integration cert.

Register: `https://meritstore.vercel.app/merit-demo/register`

## Smokes

- `GET /diag/manifest.json` — consumer, version, supabase flag
- `GET /api/meritsubs` — health
- `GET /api/meritsubs/api/v1/entitlements` — guest tier
- `/journal/` — save entry (local or Supabase)
- `/ama/` — ask + vote with privacy modes (geo-IP on Vercel)
- `/admin/` — flexible Plus pricing UI
