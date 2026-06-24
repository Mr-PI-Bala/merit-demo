# merit-demo — operator provision checklist

**Consumer:** `merit-demo` · **Reference:** freemium showcase (Angle 1–4)

## Status matrix

| Step | In-repo | Operator action |
|------|---------|-----------------|
| Legal (`portal/legal.html`, `/legal/terms`) | Done | Review copy |
| AMA geo-IP + caps + admin pricing UI | Done | Run SQL 002 |
| meritsubs embed scaffold | Done (`vendor/meritsubs`) | Vercel env + deploy |
| Supabase consumer project | SQL ready | Create project, run migrations |
| Vercel deploy | `vercel.json` + build | Set `cfg/flask_deploy.json` scope |
| meritstore tenant | `cfg/meritstore_tenant.json` seed | Vault provision after cert |
| here.now portals | `cfg/portals.json` slugs | `merit-live portal publish --all` BYOK |
| Production OAuth | Python handler | meritsubs env on Vercel |

---

## 1. Supabase (consumer project + auth path)

1. Create a **new** Supabase project for `merit-demo` (not vault SSOT).
2. SQL Editor — run in order:
   - `sql/001_merit_demo.sql`
   - `sql/002_ama_daily_activity.sql`
   - meritsubs: `AgentDraven/meritsubs/supabase/migrations/001_subscribers.sql` (same project)
3. Copy `.env.local.example` → `.env.local` with URL + keys.
4. Vercel project env: same `SUPABASE_*`, `MERIT_CONSUMER_ID=merit-demo`.
5. **Seamless auth:** meritsubs OAuth on `/api/meritsubs/api/v1/oauth/authorize` after embed deploy; journal/AMA read `Authorization: Bearer` for Plus tier.

---

## 2. Vercel deploy

```powershell
# Edit cfg/flask_deploy.json → your vercel_scope
cd merit-demo
npm run verify
.\scripts\embed-meritsubs.ps1   # if vendor/ not present
# from merit-agent-skills
.\merit-live.ps1 deploy vercel --path C:\path\to\merit-demo
```

Set Vercel env from `.env.local.example` (meritsubs JWT/API keys generated fresh).

Smokes: `GET /diag/manifest.json`, `GET /api/meritsubs/api/v1/health`, `/journal/`, `/ama/`.

---

## 3. meritstore tenant + Plus SKU

Seed: `cfg/meritstore_tenant.json` (`status: pending_platform_provision`).

**Vault operator** (after integration cert):

```powershell
.\scripts\merit.ps1 cert validate --json
# Provision merit-demo tenant on meritstore from offerings_seed
```

Register URL: `https://meritstore.vercel.app/merit-demo/register`

Admin flexible pricing: `/admin/` → saves to `operator_pricing` table; sync offerings to meritstore manually until webhook automation (Phase 3).

---

## 4. here.now (BYOK)

```powershell
$env:HERENOW_API_KEY = '...'   # or ~/.herenow/credentials
.\merit-live.ps1 portal publish --path . --all
```

Surfaces in `cfg/portals.json` (main, journal, ama, subs).

---

## 5. meritsubs production (replaces stub)

Already embedded via `scripts/embed-meritsubs.ps1`. Confirm:

```powershell
Test-Path vendor\meritsubs\api\app.py
Test-Path api\meritsubs\index.py
```

Wire `MERITSUBS_PUBLIC_BASE_URL` on meritstore for `merit-demo` consumer (MSU-MST-02).

---

## Not in v0.3.1 (deferred)

- merit-ama PAR package (v2, second consumer)
- Phase 3 meritsubs webhook entitlement keys for `@1.0.x` PAR
- GA `v1.0.0` — HumanBala approval only
