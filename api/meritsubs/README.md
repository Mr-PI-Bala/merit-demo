# meritsubs on merit-demo

## Hosted provider boundary

`api/meritsubs/index.mjs` is a thin hosted-boundary relay. It does **not** embed meritsubs provider source, Square charging logic, or usage-metering authority.

Public `merit-demo` calls hosted MERIT services for usage credits, promo validation, entitlements, and Square checkout. The default intro promo is `MERITAGENT`; the hosted provider controls the default credit amount ($25 unless changed by provider config).

If hosted entitlements are unavailable, the demo falls back to guest-only entitlements. It must never mint paid entitlements locally.

Smokes:

```powershell
$base = "https://YOUR_DEPLOY.vercel.app/api/meritsubs"
Invoke-WebRequest -Uri "$base/api/v1/health" -UseBasicParsing
```

See hosted provider/operator docs in `meritsubs docs/` and `meritstore docs/`.
