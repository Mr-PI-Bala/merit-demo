# merit-demo

Public **MERIT freemium showcase** under Mr-PI-Bala — workbench, journal, AMA, meritsubs, and meritstore. White-label operator branding with **MERIT Powered** footer (SomaTune header/footer shell).

Version: see [`VERSION`](VERSION) / [`CHANGELOG.md`](CHANGELOG.md).

Run these from the repository; the remote repo and authenticated user are inferred, and add/remove ask for confirmation:

```powershell
.\merit.ps1 admin github access add
.\merit.ps1 admin github access status
```

**Start here:** clone this repository and run one command. The consumer reads its official hosted CompatSet pins from `cfg/par_pins.json`; you do not need to clone or manually pin `merit-agent-skills` for the demo.

## Quickstart — one command

```powershell
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-demo
.\merit.ps1 quickstart
```

That command installs dependencies when needed, verifies the pinned CompatSet, builds the consumer, and starts a local HTTP server. Open the printed `/play/` URL. The page reports Hosted Ready only when the pinned hosted workbench initializes and mounts; otherwise it shows the labeled fallback.

Linux/macOS:

```bash
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-demo
./merit.sh quickstart
```

For development, install `merit-agent-skills` separately through Merit-Hub or its installer. It supplies IDE skills and release tooling; it is not required to run this static consumer showcase.

Only operators deploying their own instance need launch configuration. Edit `.merit_launch.md` and then deploy:

```powershell
.\merit.ps1 deploy --path ..\merit-demo
.\merit.ps1 portal --path ..\merit-demo
```

Linux/macOS:

```bash
./merit.sh deploy --path ../merit-demo
./merit.sh portal --path ../merit-demo
```

## Surfaces

| Route | PAR / service | here.now portal |
|-------|---------------|-----------------|
| `/play/` | merit_workbench@0.4.x | main hub |
| `/journal/` | journal@0.2.x UI; metered API from production MERIT mount | portal/journal/ |
| `/ama/` | AMA UI; metered API from production MERIT mount | portal/ama/ |
| Metered utilities | No local stub/API source; uses production MERIT Vercel mounts | — |
| Register | meritstore | portal/subs/ |

`/play/` is the canonical **Hello, meritutils** proof: DualRail `createAppShell` loads the pinned production-hosted `merit_workbench@0.4.14`, mounts the interactive shell, and reports **Hosted Ready** (or a labeled offline stub on failure). Prefer `.\merit.ps1 serve` (HTTP) — `file://` is smoke-only.

## Build & deploy

```powershell
npm install && npm run verify && npm run build
..\merit-agent-skills\merit.ps1 deploy --path .
```

Linux/macOS:

```bash
npm install && npm run verify && npm run build
../merit-agent-skills/merit.sh deploy --path .
```

Optional: Supabase per `merit-demo docs/merit_demo_usage.md` and `sql/001_merit_demo.sql`.

## Freemium → Plus

| Tier | Limits |
|------|--------|
| Guest / free | Journal 2/day; AMA 2 ask/vote/response/day; top 25 leaderboard |
| Plus ($10.79/mo) | Uncapped journal + AMA |

No seed content — operators/subscribers add their own white-label content.

## Abuse

Report to meritlabs@protonmail.com (+ operator email in `cfg/branding.json` when set).
# Developer repository access

To allow a developer account to push changes, the repository owner or an administrator must grant collaborator access:

```powershell
gh api --method PUT repos/Mr-PI-Bala/merit-demo/collaborators/AgentDraven `
  --field permission=push
```

Verify access after the invitation is accepted:

```powershell
gh api repos/Mr-PI-Bala/merit-demo --jq '.permissions'
```

`push` must be `true`. A local Git author name or a token with `repo` scope does not itself grant repository write permission. If access cannot be granted, use a writable fork and update `origin` before running release closeout.
