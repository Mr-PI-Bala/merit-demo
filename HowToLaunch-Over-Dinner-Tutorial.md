# 🍽️ Build your MERIT app over dinner

This legacy link is kept for bookmarked URLs. The beginner flow is now short, current, and powered by MERIT commands—not raw Git or retired installer scripts.

👉 **Start with the [main README](README.md)**, then follow the row that matches your goal.

## The 3×3 dinner path

Read each row from left to right: **Start → Make it → Finish**.

| Your goal | 1. Start | 2. Make it | 3. Finish |
|---|---|---|---|
| 👀 **Try the demo** | Download [Merit-Hub.ps1](https://raw.githubusercontent.com/AgentDraven/merit-agent-skills/main/Merit-Hub/Merit-Hub.ps1), open PowerShell, run `.\Merit-Hub.ps1`, choose **3** | Run `.\merit.ps1 serve` | Open the printed `/play/` link |
| 🛠️ **Build an app** | Run Hub, choose **3**, then open this folder | Edit `cfg/`, `portal/`, or `play/` | Run `.\merit.ps1 verify` |
| ☁️ **Publish my version** | Verify your local changes | Run `.\merit.ps1 closeout` | Run `.\merit.ps1 deploy` (publish `portal/` when ready) |

### Optional: add IDE help

IDE skills are optional for any row. Download and run **Merit-Hub.ps1**, then choose **I — Install IDE skills**. The Hub detects the available IDE and installs the supported adapter. See the [skills guide](https://github.com/AgentDraven/merit-agent-skills#start-here).

## What the commands do

| Command | Friendly meaning |
|---|---|
| `.\Merit-Hub.ps1` | Opens the guided MERIT menu and can fetch missing PowerShell support. |
| `.\merit.ps1 serve` | Serves the demo over local HTTP and prints the browser URL. |
| `.\merit.ps1 verify` | Checks the consumer scaffold and configured CompatSet pins. |
| `.\merit.ps1 closeout` | Runs verification, tests, 3-3 evidence, changelog/status checks, and creates a release receipt. |
| `.\merit.ps1 deploy` | Deploys the verified consumer when cloud credentials are configured. |

## If something gets stuck

1. Copy the exact command output.
2. Run `.\merit.ps1 where` to show the active MERIT surfaces.
3. Run `.\merit.ps1 closeout` again after the fix.

For deeper troubleshooting, use [merit_demo_usage.md](merit-demo%20docs/merit_demo_usage.md) and the controlling [ecosystem IAR](merit-demo%20docs/IAR/MERIT_DEMO_ECOSYSTEM_PLAN.md).

> **Old guide cleanup:** raw `git clone`, `install.ps1`, `install.sh`, and the retired `skills-v0.3.14` pin are intentionally not documented here. Hub and `merit.ps1` now own setup and validation.
