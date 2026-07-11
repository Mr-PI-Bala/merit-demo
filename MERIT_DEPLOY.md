# MERIT_DEPLOY

One human-edited deploy profile for `merit-demo`.

Edit this file first, then sync generated config:

```powershell
..\merit-agent-skills\merit-deploy.ps1 sync --path .
..\merit-agent-skills\merit-deploy.ps1 vercel --path .
..\merit-agent-skills\merit-deploy.ps1 portal --path . --all
```

Linux/macOS:

```bash
../merit-agent-skills/merit-deploy.sh sync --path .
../merit-agent-skills/merit-deploy.sh vercel --path .
../merit-agent-skills/merit-deploy.sh portal --path . --all
```

Do not put real secrets in this file. Use `.env.local`, Vercel env, Supabase, and here.now credentials for secrets.

## Vercel app host

<!-- MERIT_DEPLOY:vercel -->
```json
{
  "project_id": "merit-demo",
  "vercel_scope": "REPLACE_WITH_YOUR_VERCEL_TEAM",
  "production_branch": "main",
  "notes": "Run npx vercel link --scope REPLACE_WITH_YOUR_VERCEL_TEAM once. Vercel creates .vercel/project.json."
}
```
<!-- /MERIT_DEPLOY:vercel -->

## here.now marketing portals

<!-- MERIT_DEPLOY:portals -->
```json
{
  "schema": "merit.portals.v1",
  "surfaces": [
    { "id": "main", "path": "portal/", "slug": "merit-demo" },
    { "id": "journal", "path": "portal/journal/", "slug": "merit-demo-journal" },
    { "id": "ama", "path": "portal/ama/", "slug": "merit-demo-ama" },
    { "id": "subs", "path": "portal/subs/", "slug": "merit-demo-subs" }
  ],
  "notes": "Publishing requires HERENOW_API_KEY or ~/.herenow/credentials."
}
```
<!-- /MERIT_DEPLOY:portals -->

## Credentials checklist

Use provider CLIs and dashboards for secrets:

- Vercel: authenticated CLI session and one-time `npx vercel link --scope <scope>`.
- here.now: `HERENOW_API_KEY` or `~/.herenow/credentials`.
- Supabase: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.
- meritsubs: `MERITSUBS_PUBLIC_BASE_URL`, `MERITSUBS_JWT_SECRET`, `MERITSUBS_API_KEY`, `MERITSUBS_ADMIN_KEY`.
