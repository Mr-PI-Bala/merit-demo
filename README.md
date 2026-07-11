# merit-demo

Public **MERIT freemium showcase** under Mr-PI-Bala — workbench, journal, AMA, meritsubs, and meritstore. White-label operator branding with **MERIT Powered** footer (SomaTune header/footer shell).

**Start here** after cloning [merit-agent-skills](https://github.com/AgentDraven/merit-agent-skills).

## Quickstart

```powershell
git clone --branch skills-v0.3.4 https://github.com/AgentDraven/merit-agent-skills.git
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-agent-skills
.\install.ps1 -Target Cursor
.\merit-live.ps1 par scaffold --path ..\merit-demo --variant workbench-journal
.\merit-live.ps1 branding scaffold --path ..\merit-demo
.\merit-live.ps1 subs scaffold --path ..\merit-demo
.\merit-live.ps1 verify --path ..\merit-demo
```

Linux/macOS:

```bash
git clone --branch skills-v0.3.4 https://github.com/AgentDraven/merit-agent-skills.git
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-agent-skills
./install.sh -Target Cursor
./merit-live.sh par scaffold --path ../merit-demo --variant workbench-journal
./merit-live.sh branding scaffold --path ../merit-demo
./merit-live.sh subs scaffold --path ../merit-demo
./merit-live.sh verify --path ../merit-demo
```

Edit `cfg/branding.json`, `cfg/flask_deploy.json` (your Vercel scope), and `cfg/portals.json` slugs. Deploy:

```powershell
.\merit-live.ps1 deploy vercel --path ..\merit-demo
.\merit-live.ps1 portal publish --path ..\merit-demo --all
```

Linux/macOS:

```bash
./merit-live.sh deploy vercel --path ../merit-demo
./merit-live.sh portal publish --path ../merit-demo --all
```

## Surfaces

| Route | PAR / service | here.now portal |
|-------|---------------|-----------------|
| `/play/` | merit_workbench@0.4.x | main hub |
| `/journal/` | journal@0.2.x + `/api/journal` | portal/journal/ |
| `/ama/` | AMA API + journal patterns | portal/ama/ |
| `/api/meritsubs` | entitlements stub → wire production meritsubs | — |
| Register | meritstore | portal/subs/ |

## Build & deploy

```powershell
npm install && npm run verify && npm run build
.\merit-live.ps1 deploy vercel --path .   # from merit-agent-skills; your Vercel scope
```

Linux/macOS:

```bash
npm install && npm run verify && npm run build
../merit-agent-skills/merit-live.sh deploy vercel --path .
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
