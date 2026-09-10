# merit-demo

Public **MERIT freemium showcase** under Mr-PI-Bala — workbench, journal, AMA, meritsubs, and meritstore. White-label operator branding with **MERIT Powered** footer (SomaTune header/footer shell).

Version: **0.3.28** — see [`VERSION`](VERSION) / [`CHANGELOG.md`](CHANGELOG.md).

### New user guides

- [Quick Start](merit-demo%20docs/QUICK_START.md) — the short, pictorial path from local launch to provider checks.
- [Detailed Walkthrough](merit-demo%20docs/DETAILED_WALKTHROUGH.md) — personas, flowcharts, commands, screenshots, and alpha gates.
- [Alpha executive summary](merit-demo%20docs/IAR/evidence/ALPHA-2026-09-09.md) — exact hosted scenarios, results, and remaining blockers.

<a id="start-here-choose-your-path"></a>
<table><tr><td bgcolor="#1f6feb"><strong><big><big>🧭 Start here — choose your path</big></big></strong></td></tr></table>

The three rows are three fun ways to use MERIT. Read left to right: **Start → Make it → Finish**.

| Your goal | Start here | Make progress | Finish with |
|---|---|---|---|
| 👀 **Try the demo** | [Download the Hub](https://github.com/AgentDraven/merit-agent-skills/blob/main/Merit-Hub/Merit-Hub.ps1), run `.\Merit-Hub.ps1`, choose **Try it** (the menu item that starts this demo) | [Run the quickstart](#see-the-demo) | [Open `/play/`](#see-the-demo) |
| 🛠️ **Build an app** | [Run the Hub](https://github.com/AgentDraven/merit-agent-skills#start-here--pick-your-adventure), choose **Try it** to open this repo | [Edit branding, app, and `cfg/`](#build-on-the-template) | [Run `.\merit.ps1 verify`](#build-on-the-template) |
| ☁️ **Publish my version** | [Verify locally](#build-on-the-template) | [Run `.\merit.ps1 closeout`, then `deploy`](#deploy-your-version) | [Publish `portal/`](#deploy-your-version) |

> Optional: install IDE skills from [`merit-agent-skills`](https://github.com/AgentDraven/merit-agent-skills#i-want-skills-in-my-ide). The app works without them.

### See the demo

**One-command path after the Hub has seeded the repo:**

```powershell
.\merit.ps1 serve
```

Then open the printed `/play/` address. If you are starting from a new laptop, download and run the Hub first, then choose **Try it** (the action that clones this repo, starts the local page, and opens the demo).

### The three-step cards (what each path actually does) 🧩

Every beginner path follows the same **Start → Make progress → Finish** rhythm. Each card below has three concrete checks, so you always know what “done” looks like.

#### 👀 Try the demo

1. **Start**
   - Open PowerShell and run `.\Merit-Hub.ps1`.
   - Choose **Set up this laptop** to prepare the local MERIT folder, then choose **Get the free MERIT tools** if this is a new laptop.
   - Choose **Try it** to reuse the existing clean demo folder, start local HTTP, and open the consumer page.
2. **Make progress**
   - The Hub starts the local HTTP server on its reusable port.
   - Open the printed `/play/` URL in a browser.
   - Confirm the page says **Hosted Ready** and shows the MERIT workbench.
3. **Finish**
   - Run **Validate my local demo** to check the routes, hosted workbench, registration link, and local fallback.
   - Try **Register free** to see the hosted registration route.
   - Use **OSS in Cloud** only when you want the hosted consumer activation journey.

#### 🛠️ Build an app

1. **Start**
   - Keep this repository as your clean consumer starting point.
   - Review `cfg/branding.json` and the `play/` and `portal/` shells.
   - Make a small, friendly change (name, colors, or welcome copy).
2. **Make progress**
   - Run `.\merit.ps1 verify` after each change.
   - Check that local routes still load through `.\merit.ps1 serve`.
   - Keep generated receipts and configuration changes explainable.
3. **Finish**
   - Run `.\merit.ps1 closeout` to verify the release state.
   - Review the printed commit, branch, and hosted-pin evidence.
   - Continue to deployment only after closeout reports success.

#### ☁️ Publish my version

1. **Start**
   - Finish the local build and verification checks first.
   - Confirm the tested-together tool version and the production MERIT address.
   - Sign in to the target hosting account only when publishing is intended.
2. **Make progress**
   - Run **OSS in Cloud** from the Hub for the hosted OSS path, or use the deploy command for your own host.
   - Watch the live play, register, and marketing URLs printed by the Hub.
   - If a publish step fails, rerun the named phase after fixing the reported cause.
3. **Finish**
   - Run **Walk through my hosted demo** to validate every hosted endpoint in order.
   - Confirm the receipt records the consumer id and all live URLs.
   - Share the hosted link only after the final closeout and 3-3 summary.

#### 🧠 Optional IDE skills helper

1. **Start**
   - Download and run the Hub from `merit-agent-skills`.
   - Choose **I — Install IDE skills** and select your host.
   - Leave this step out if you only want the demo.
2. **Make progress**
   - The Hub writes skills to the host’s supported location.
   - Keep the consumer repo independent from host-specific files.
   - Re-run the installer when the skills pin is intentionally upgraded.
3. **Finish**
   - Ask your IDE to follow the MERIT closeout and 3-3 law.
   - Verify the installed host status when the adapter supports it.
   - Treat unsupported hosts as guidance-only and use `merit.ps1 closeout`.

### Build on the template

Start with `play/`, `portal/`, and `cfg/par_pins.json`. The tested tool version is already selected; you do not need to manually clone or choose a version of `merit-agent-skills`.

### Member session and hosted actions

Journal and AMA use MERIT's public gateway rails: `/api/gw/journal` and `/api/gw/ama`. Each request carries the configured `consumer_id`; a provider bearer token is added only after the visitor chooses a member or guest session in the **Try this app as a member** panel. Tokens stay in browser `sessionStorage` for that consumer and are never written to the repository, `localStorage`, or a URL.

The panel explains three choices in plain language:

- **Open hosted registration** opens the live `/store/<consumer_id>/register` page.
- **Continue with email** requests the provider's registered-member session.
- **Start guest preview** requests a provider guest session; if the provider is unavailable, the page remains usable in labeled local-demo mode.

The provider owns identity, entitlements, quotas, persistence, and tenant isolation. A fork changes the values in `cfg/merit-sync.json` and branding; the session bridge derives its routes from those values.

### Make this app yours

The smallest fork changes three files:

1. Open `cfg/branding.json` and change the product name, colors, welcome words, and abuse contact.
2. Open `cfg/merit-sync.json` and set your own `consumer_id` and the provider URLs supplied by MERIT. Keep the registration URL under your app's provider path.
3. Run `.\merit.ps1 verify`, then open `.\merit.ps1 serve` and check `/play/`, `/journal/`, `/ama/`, and `/portal/`.

For a hosted app, use the Hub's **OSS in Cloud** action. This checkout uses the live reference tenant `merit-demo-alpha`; the repository slug `merit-demo` is reserved as a provider showcase alias. The Hub creates or reuses your app identity and prints the matching play, registration, and marketing URLs. A fork must use its own app identity before inviting subscribers. Keep provider activation, identity, limits, and checkout on MERIT services. The fork only owns its branding, copy, and consumer presentation.

### Deploy your version

Use `.\merit.ps1 closeout`, then `.\merit.ps1 deploy`, and finally `.\merit.ps1 portal` only when you are ready to publish your own instance.

<details><summary>Additional options and administration</summary>

Repository administration commands infer the remote and authenticated user; add/remove ask for confirmation:

```powershell
.\merit.ps1 admin github access add
.\merit.ps1 admin github access status
```

Switch the GitHub account used for repository administration without calling `gh` directly:

```powershell
.\merit.ps1 admin github auth status
.\merit.ps1 admin github auth switch
```

</details>

For Linux/macOS, use `./merit.sh quickstart`. Deployment details are in [merit_demo_usage.md](merit-demo%20docs/merit_demo_usage.md).

<table><tr><td bgcolor="#0d9488"><strong><big><big>🧩 Surfaces</big></big></strong></td></tr></table>

| Route | PAR / service | here.now portal |
|-------|---------------|-----------------|
| `/play/` | merit_workbench@0.4.x | main hub |
| `/journal/` | journal@0.2.x UI; metered API from production MERIT mount | portal/journal/ |
| `/ama/` | AMA UI; metered API from production MERIT mount | portal/ama/ |
| Metered utilities | No local stub/API source; uses production MERIT Vercel mounts | — |
| Register | meritstore | portal/subs/ |

`/play/` is the main **Hello, meritutils** check: DualRail `createAppShell` loads the production-hosted `merit_workbench@0.4.14`, mounts the interactive shell, and reports **Hosted Ready** (or a clear offline message if it cannot). Prefer `.\merit.ps1 serve` (HTTP) — opening the file directly is only a quick visual look.

<table><tr><td bgcolor="#0d9488"><strong><big><big>🚀 Build & deploy</big></big></strong></td></tr></table>

```powershell
.\merit.ps1 verify
..\merit-agent-skills\merit.ps1 deploy --path .
```

Linux/macOS:

```bash
./merit.ps1 verify
../merit-agent-skills/merit.sh deploy --path .
```

Optional: Supabase per `merit-demo docs/merit_demo_usage.md` and `sql/001_merit_demo.sql`.

<table><tr><td bgcolor="#0d9488"><strong><big><big>💎 Freemium → Plus</big></big></strong></td></tr></table>

| Visitor type | Limits |
|------|--------|
| Guest / free | Journal 2/day; AMA 2 ask/vote/response/day; top 25 leaderboard |
| Plus ($10.79/mo) | Uncapped journal + AMA |

No seed content — operators/subscribers add their own white-label content.

<table><tr><td bgcolor="#0d9488"><strong><big><big>🛟 Abuse</big></big></strong></td></tr></table>

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
