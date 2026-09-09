## [0.3.27] — 2026-09-09

### Added
- Add pictorial Quick Start and Detailed Walkthrough guides with Mermaid pathways, persona steps, screenshots, and alpha release gates.
- Add the hosted deployment validation executive summary and machine-readable scenario evidence.

### Changed
- Link the new guides and current validation evidence from the README and documentation index.
- Keep the README release banner aligned with VERSION and package metadata.

## [0.3.25] — 2026-09-09

### Added
- Add a branded /play/ welcome flow with clear Journal, AMA, registration, and hosted-workbench paths.
- Add a provider-backed member session bridge using consumer-scoped sessionStorage and dynamic gateway routes.

### Fixed
- Make alpha session smoke report a precise gateway-health blocker when the provider route is not deployed.
- Replace cryptic Hub menu numbers in the beginner usage path with the action names and outcomes.

## [0.3.24] — 2026-09-08

### Fixed
- Keep the explicit free-registration smoke generic for forked consumer IDs; the idempotency key now derives from the configured tenant and the fork contract rejects reference-tenant hardcoding.

## [0.3.23] — 2026-09-08

### Fixed
- Align the README release banner with VERSION, package metadata, and the tested release tag.

## [0.3.22] — 2026-09-08

### Changed
- Activated the app-specific provider tenant `merit-demo-alpha` and aligned the consumer/provider contract, registration CTA, diagnostics, and portal publication slugs with that live tenant.
- Kept the repository name `merit-demo` separate from the provider's reserved showcase slug; forks must set their own `consumer_id` and registration URL.
- Made alpha contract checks derive identity from consumer configuration instead of asserting a generic hardcoded slug.
- Kept browser evidence under the repository-owned `merit-demo docs/evidence/` path when a fork changes its provider identity.

## [0.3.21] — 2026-09-08

### Fixed
- Make branding, consumer identity, registration paths, and local storage fork from generated configuration instead of keeping reference deployment URLs in the visitor surfaces.
- Make the portal tree render correctly when served from Vercel `/`, Vercel `/portal/`, or an independently published here.now site rooted at `portal/`.
- Add styled AMA, Journal, and Membership marketing pages plus dynamic legal and terms links.
- Add fork-contract and browser outage tests, including local Journal save and AMA post behavior.

## [0.3.20] — 2026-09-08

### Fixed
- Ship the portal's CSS, JavaScript, and config with the Vercel build so `/` and `/portal/` render the same branded consumer shell.
- Make Journal and AMA local-first when provider routes are unavailable, with explicit cloud, local, limit, and error states.
- Make browser registration checks fail closed when merit-prod redirects the expected consumer route to the developer guide.
- Record the current `merit-demo` commerce tenant as pending provider activation instead of claiming registration is ready.

## [0.3.19] — 2026-09-08

### Fixed
- Make the consumer-owned alpha registration contract test report a normal non-zero result on Windows while allowing fetch cleanup to finish.

# Changelog

## [0.3.17] — 2026-09-08

### Fixed
- Added a shared consumer API helper that sends `X-Merit-Consumer`, preserves browser credentials, and forwards an available platform session token to hosted journal/AMA APIs.
- Replaced unsafe AMA API-data `innerHTML` interpolation with safe text and DOM rendering.
- Added the alpha consumer contract test and documented the `merit-demo` / `merit-test` trial matrix.

The `merit-demo` registration tenant still redirects to the provider commerce guide; the live trial test remains OPEN until provider provisioning is repaired.

## [0.3.18] — 2026-09-08

### Changed
- Moved the consumer/provider registration contract into `merit-demo`, where `consumer_id`, provider URLs, and expected registration behavior belong.
- Replaced the generic skills trial matrix with a consumer-owned provider contract test.


## [0.3.16] — 2026-09-08

### Added
- Gaps to Alpha in the controlling consumer IAR: owned bugs/FRs, red-first TDD gates, eight persona pathways, and future vault extraction requirements.
- Explicit standard OC independence from any local private-vault checkout, runtime or operator secrets; hosted provider dependencies remain documented.

### Fixed
- Repaired MERIT usage-guide hyperlink pairs and IAR anchor formatting.
- Corrected validation-only closeout guidance and aligned VERSION, package metadata, lockfile and README on 0.3.16.

Alpha requirements remain OPEN. This documentation and release-hygiene patch does not implement subscriber registration, identity, payment or entitlement fixes.

## [0.3.15] — 2026-09-07

- Added three-step pathway cards with concrete Start, Make progress, and Finish checks for demo, build, publish, and IDE journeys.

## [0.3.14] — 2026-09-07

- Added beginner guidance for when OSS users should consider Vault/VC.

## [0.3.13] — 2026-09-07

- Promoted the hosted OC tutorial from planned to available documentation.

## [0.3.12] — 2026-09-07

- Documented hosted OC tutorial ownership and walkthrough behavior.

## [0.3.11] — 2026-09-06

- Documented Step 3 cloud-first architecture and Hub HTTP server evidence behavior.

## [0.3.10] — 2026-09-06

### Fixed
- Aligned `VERSION`, `package.json`, and `package-lock.json` so release and runtime reports use the same version.

All notable changes to **merit-demo** (public MERIT freemium showcase consumer).

Format: Keep a Changelog–style sections under each version. Versions align with `VERSION` / `package.json`.

## [0.3.8] — 2026-09-06

### Changed
- Reworked the README diagram into a colorful sequential three-row learning flow.
- Reworked README onboarding into a persona-based flow with progressive disclosure.

### Fixed
- Added a historical release index for tags `v0.3.0`–`v0.3.2` that predate detailed changelog sections.

- Added one-command `merit.ps1 quickstart` / `merit.sh quickstart` for dependency setup, CompatSet verification, and local HTTP launch.
- Simplified README Quickstart; hosted package versions remain controlled by `cfg/par_pins.json`.

### Fixed
- Consumer release authority now prefers the vault operator CLI when a vault is present, otherwise the OSS skills CLI.
- GitHub access/authentication commands are documented behind `merit.ps1`.

## [0.3.4] — 2026-09-05

### Added
- DualRail Gloss play bootstrap: `merit_ux@0.1.3` `createAppShell` + mounted `merit_workbench@0.4.0` from `merit-prod.vercel.app`
- Runtime states on `/play/`: Checking → Hosted Ready / Demo Fallback / Runtime Unavailable (labeled offline stub with retry + portal link)
- `.\merit.ps1 serve` (alias `play`) — build + local HTTP server for Hosted Ready proof without exposing tool-chain commands
- Controlling IAR SSOT: `merit-demo docs/IAR/MERIT_DEMO_ECOSYSTEM_PLAN.md` (zones A–D FR matrix, Codex merge changelog)
- Generated root `config.js` (gitignored) alongside `dist/config.js` for repo-root HTTP serve
- Playwright assertions for Hosted Ready, workbench mount, and Register free

### Changed
- README / usage / design / AGENTS: path resolve via `MYMERITAPP` / `oss-bench`, skills pin **skills-v0.5.66**, prefer `merit.ps1` verbs over raw implementation commands
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
