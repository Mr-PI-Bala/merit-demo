# meritsubs on merit-demo

## Stub mode (default until embed)

`api/meritsubs/index.mjs` — guest/subscriber health + entitlements for local dev without Python.

## Production embed (SomaTune pattern)

```powershell
# From meritsubs repo
.\scripts\embed-merit-demo.ps1

# Or from merit-demo
.\scripts\embed-meritsubs.ps1
```

Replaces `index.mjs` with `index.py` + `vendor/meritsubs/`. Set Vercel env per `.env.local.example`.

Smokes:

```powershell
$base = "https://YOUR_DEPLOY.vercel.app/api/meritsubs"
Invoke-WebRequest -Uri "$base/api/v1/health" -UseBasicParsing
```

See `meritsubs docs/consumers/SOMATUNE_EMBED.md` and vault `templates/legal/`.
