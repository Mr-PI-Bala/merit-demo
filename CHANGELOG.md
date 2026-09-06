# Changelog

All notable changes to **merit-demo** (public MERIT freemium showcase consumer).

Format: Keep a Changelog–style sections under each version. Versions align with `VERSION` / `package.json`.

## [0.3.6] — 2026-09-06

### Fixed
- Added a historical release index for tags `v0.3.0`–`v0.3.2` that predate detailed changelog sections.

### Changed
- Added one-command `merit.ps1 quickstart` / `merit.sh quickstart` for dependency setup, CompatSet verification, and local HTTP launch.
- Simplified README Quickstart; hosted package versions remain controlled by `cfg/par_pins.json`.

### Fixed
- Consumer release authority now prefers the vault operator CLI when a vault is present, otherwise the OSS skills CLI.
- GitHub access/authentication commands are documented behind `merit.ps1`.

## [0.3.4] — 2026-09-05

### Added
- DualRail Gloss play bootstrap: `merit_ux@0.1.3` `createAppShell` + mounted `merit_workbench@0.4.0` from `merit-prod.vercel.app`
- Runtime states on `/play/`: Checking → Hosted Ready / Demo Fallback / Runtime Unavailable (labeled offline stub with retry + portal link)
- `.\merit.ps1 serve` (alias `play`) — build + local HTTP server for Hosted Ready proof without typing raw npm/npx
- Controlling IAR SSOT: `merit-demo docs/IAR/MERIT_DEMO_ECOSYSTEM_PLAN.md` (zones A–D FR matrix, Codex merge changelog)
- Generated root `config.js` (gitignored) alongside `dist/config.js` for repo-root HTTP serve
- Playwright assertions for Hosted Ready, workbench mount, and Register free

### Changed
- README / usage / design / AGENTS: path resolve via `MYMERITAPP` / `oss-bench`, skills pin **skills-v0.5.66**, prefer `merit.ps1` verbs over raw npm
- `scripts/build.mjs`: richer `MERIT_DEMO_CONFIG` (par pins, health URL, portal URL); copy `merit-surface.css` into dist
- `scripts/e2e-smoke.mjs` / `e2e-playwright.mjs`: DualRail + mount checks
- IAR `SOTU.md`: Pass 1 Hosted Ready note
- Docs INDEX links ecosystem plan IAR

### Fixed
- Endless “Loading workbench…” when CDN package loaded but nothing mounted into the play host

## [0.3.3] — prior

Baseline public showcase before Pass 1 DualRail Hosted Ready work (Hello World CDN presence without interactive mount).

## Historical release index

The original demo tags `v0.3.0`, `v0.3.1`, and `v0.3.2` predate the current detailed changelog sections. Their tag history remains immutable and is the source of exact historical diffs; future releases must have a dedicated version section.
