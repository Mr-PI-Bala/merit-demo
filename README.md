# merit-demo

Public **MERIT freemium showcase** under Mr-PI-Bala — workbench, journal, AMA, meritsubs, and meritstore. White-label operator branding with **MERIT Powered** footer (SomaTune header/footer shell).

**Start here** after cloning [merit-agent-skills](https://github.com/AgentDraven/merit-agent-skills).

## Quickstart

```powershell
git clone --branch skills-v0.3.14 https://github.com/AgentDraven/merit-agent-skills.git
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-agent-skills
.\install.ps1 -Target Cursor
.\merit.ps1 init --path ..\merit-demo
# edit ..\merit-demo\.merit_launch.md
.\merit.ps1 apply --path ..\merit-demo
.\merit.ps1 verify --path ..\merit-demo
```

Linux/macOS:

```bash
git clone --branch skills-v0.3.14 https://github.com/AgentDraven/merit-agent-skills.git
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-agent-skills
./install.sh -Target Cursor
./merit.sh init --path ../merit-demo
# edit ../merit-demo/.merit_launch.md
./merit.sh apply --path ../merit-demo
./merit.sh verify --path ../merit-demo
```

Edit only `.merit_launch.md` for launch/deploy values. It is local, gitignored, and includes comments/examples. Then deploy:

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

`/play/` is the canonical **Hello, meritutils** proof: it loads the production-hosted `merit_workbench@0.4.0` package and reports readiness in the page before the interactive workbench.

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
