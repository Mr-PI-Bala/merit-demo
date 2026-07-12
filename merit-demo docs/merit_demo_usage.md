# merit-demo — usage

`merit-demo` is the public hello-world consumer for MERIT Agent Skills and MERIT Prod. It shows workbench, journal, AMA, Portal, legal pages, and the production registration path without exposing provider billing or metered utility source code.

## 3 Steps Over Dinner

### 1. Local Setup

Create an empty working directory and clone the public skills repo plus this demo:

```powershell
mkdir C:\MeritOverDinner
cd C:\MeritOverDinner
git clone --branch skills-v0.3.11 https://github.com/AgentDraven/merit-agent-skills.git
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-agent-skills
.\install.ps1 -Target Cursor
.\merit.ps1 verify --path ..\merit-demo
```

Linux/macOS:

```bash
mkdir -p ~/MeritOverDinner
cd ~/MeritOverDinner
git clone --branch skills-v0.3.11 https://github.com/AgentDraven/merit-agent-skills.git
git clone https://github.com/Mr-PI-Bala/merit-demo.git
cd merit-agent-skills
./install.sh -Target Cursor
./merit.sh verify --path ../merit-demo
```

### 2. Initialize The Repository

`.merit_launch.md` is the one private file you edit. It creates the other required local/machine files for this repo, including `.env.local`, `cfg/flask_deploy.json`, and `cfg/portals.json`.

```powershell
.\merit.ps1 init --path ..\merit-demo
# edit ..\merit-demo\.merit_launch.md mandatory section
.\merit.ps1 apply --path ..\merit-demo
npx vercel link --scope <your-vercel-scope>
.\merit.ps1 deploy --path ..\merit-demo
```

Linux/macOS:

```bash
./merit.sh init --path ../merit-demo
# edit ../merit-demo/.merit_launch.md mandatory section
./merit.sh apply --path ../merit-demo
npx vercel link --scope <your-vercel-scope>
./merit.sh deploy --path ../merit-demo
```

`apply` can generate MERIT config, but Vercel still owns `.vercel/project.json`; run `npx vercel link` once before the first cloud deploy.

### 3. Add Marketing Front-End & Save

Edit the demo Portal in `portal/` when you want a public marketing face:

```powershell
# edit ..\merit-demo\portal\index.html and portal.json
.\merit.ps1 portal --path ..\merit-demo
git -C ..\merit-demo status
git -C ..\merit-demo add .
git -C ..\merit-demo commit -m "launch: update Portal"
git -C ..\merit-demo push
```

Use `merit-closeout` only if you are operating inside the private MERIT vault workflow. Public creators can use normal Git status/add/commit/push.

## Provider and usage boundary

Missing promo codes resolve to `MERITAGENT`, and usage attribution reports affiliate code `MERITDEMO`. The hosted provider controls the intro credit budget (default $25) and Square checkout; this public repo does not expose or own billing logic.

Production handler policy: public `merit-demo` ships no local meritsubs, AMA, journal, leaderboard, DIRT, or other metered utility handlers. The static shell calls production MERIT Vercel mounts via `MERIT_METERED_API_BASE_URL` and `MERITSUBS_PUBLIC_BASE_URL`.

Register path: `https://merit-prod.vercel.app/store/merit-demo/register`

## Build

```powershell
npm install
npm run verify
npm run build
npm run e2e
```

## Optional Supabase

For cloud journal/AMA persistence, create your own Supabase project and run:

- `sql/001_merit_demo.sql`
- `sql/002_ama_daily_activity.sql`

Then set the Supabase values in `.merit_launch.md` and run `merit apply`.
