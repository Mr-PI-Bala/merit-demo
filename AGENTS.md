# AGENTS.md

L3: **merit-demo** — MERIT freemium showcase consumer.

- Design: `merit-demo docs/merit_demo_design.md`
- Usage: `merit-demo docs/merit_demo_usage.md`
- Plan SSOT: `merit-demo docs/IAR/MERIT_DEMO_ECOSYSTEM_PLAN.md`
- OSS CLI: sibling [merit-agent-skills](https://github.com/AgentDraven/merit-agent-skills) `merit.ps1` / `merit.sh` (pin via `%MYMERITAPP%\oss-bench.json`)

**Paths:** resolve `MYMERITAPP` → `oss-bench.json` → `demoFolder`; or `..\merit-agent-skills\merit.ps1 where`. Never hardcode `C:\MyMeritApp`.

**Skills host:** Hub **I** / `install.ps1 -Target Cursor` → `~/.cursor/skills` (not a full in-repo `.cursor` skill tree).

Public users use **merit.ps1** / **merit.sh** for scaffold/deploy; vault **scripts/merit.ps1** is only for private cert and operator-gate workflows.
