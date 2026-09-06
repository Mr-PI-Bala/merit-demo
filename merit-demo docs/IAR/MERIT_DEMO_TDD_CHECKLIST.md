# MERIT Demo Zone TDD Checklist

**Status:** Active test authority  
**Owner:** merit-demo consumer / MERIT ecosystem maintainers  
**Controlling plan:** [MERIT Demo Ecosystem Plan](MERIT_DEMO_ECOSYSTEM_PLAN.md)  
**Last updated:** 2026-09-06

This is the executable acceptance checklist for Zones A–D. A requirement is not complete because prose says it is complete: each row needs a reproducible check and evidence. Status values are `PASS`, `FAIL`, `BLOCKED`, `OPEN`, or `N/A`.

## How to run the TDD loop

For every row:

1. Run the listed command or perform the manual check and record the initial result.
2. If it fails, implement the smallest fix in the owning zone.
3. Rerun the same check.
4. Attach evidence under `merit-demo docs/IAR/evidence/` or link to an external receipt.
5. Change the row status only when the expected result is observed.

Zone completion requires every P0 row to pass. P1/P2 rows must pass or have an explicit approved disposition in the controlling IAR.

## Commands and prerequisites

The public consumer workflow is `merit.ps1`. Run these from the `merit-agent-skills` checkout:

```powershell
$skills = 'C:\DApps\merit-agent-skills'
$repo = 'C:\DApps\merit-demo'

& "$skills\merit.ps1" where
& "$skills\merit.ps1" verify --path $repo
& "$skills\merit.ps1" closeout --path $repo
```

`verify` validates the public MERIT scaffold. `closeout` runs verify plus whitespace validation and is validation-only; it does not run browser E2E or deploy anything. `law closeout` prints the OSS closeout law and is not itself a test runner.

The repository-level implementation tests are the lower-level checks called by or supplementing the public CLI. Run these from `C:\DApps\merit-demo`:

```powershell
npm run verify
npm run e2e
$env:PLAYWRIGHT_EXECUTABLE_PATH="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
npm run e2e:playwright
```

### Public CLI equivalence map

| TDD purpose | Consumer-facing command | Current implementation-level equivalent | Notes |
|---|---|---|---|
| Surface discovery | `merit.ps1 where` | — | Zone A prerequisite; confirms OSS bench, IDE, vault, Hub, and consumer surfaces |
| Scaffold verification | `merit.ps1 verify --path C:\DApps\merit-demo` | `npm run verify` | `merit.ps1` is the required public gate; npm is the repo-level detail |
| Validation closeout | `merit.ps1 closeout --path C:\DApps\merit-demo` | `git diff --check` plus `verify` | Does not include browser E2E, cloud checks, or deployment |
| Local static smoke | No current public CLI verb | `npm run e2e` | This capability should be exposed or documented as a supported skill/CLI subcommand |
| Browser E2E | No current public CLI verb | `npm run e2e:playwright` | README advertises `merit.ps1 e2e`, but v0.5.66 rejects that command; track as B-TDD-07 |
| Vercel deployment | `merit.ps1 deploy --path ...` | Vercel CLI/deploy skill internals | Mutating; run only with deployment approval |
| here.now publication | `merit.ps1 portal --path ...` | here.now publisher internals | Mutating; run only with portal-publication approval |

The missing public `e2e` verb is a merit-agent-skills enhancement, not a reason to claim Zone C complete. Until it exists, record both the public CLI result and the npm implementation result.

For deployed smoke checks, set `MERIT_CONSUMER_BASE_URL` before `npm run e2e`. The `file://` protocol is smoke-only; browser acceptance must use local HTTP or a deployed HTTPS origin.

## Zone A — Hub, laptop, and Cursor follow-through

| ID | Pri | FR | Check / command | Expected result | Evidence | Status | Remediation |
|---|---|---|---|---|---|---|---|
| A-TDD-01 | P0 | FR-001-A | Resolve `%MYMERITAPP%`, read `oss-bench.json`, resolve `demoFolder` | Resolved path equals the seeded consumer repo; no hardcoded `C:\MyMeritApp` | Hub receipt + PowerShell output | OPEN | Fix Hub path resolution and receipt |
| A-TDD-02 | P0 | FR-002-A | Inspect `~/.cursor/skills` and required retained skills | Skills are installed on the IDE skills host, not assumed to be vendored in the repo | Skill listing + version output | OPEN | Repair install/scaffold validation |
| A-TDD-03 | P0 | FR-003-A | Open Cursor using the resolved `demoFolder` | Cursor opens `C:\DApps\merit-demo` (or the resolved equivalent) | Cursor workspace/task evidence | OPEN | Fix Hub “Open in Cursor” follow-through |
| A-TDD-04 | P1 | FR-011-A | Serve the repo over local HTTP and open `/`, `/play/`, `/journal/`, `/ama/` | Each route loads from HTTP with no file-protocol dependency | Browser or Playwright route output | OPEN | Fix local serve instructions or route packaging |
| A-TDD-05 | P1 | FR-001-A | Run `Get-Location` and `Get-Content .\AGENTS.md` in a fresh Codex task | Both commands succeed without setup-refresh or workspace errors | Captured task output | OPEN | Repair workspace/sandbox ownership before continuing |

## Zone B — merit-agent-skills, Hub scripts, and documentation

| ID | Pri | FR | Check / command | Expected result | Evidence | Status | Remediation |
|---|---|---|---|---|---|---|---|
| B-TDD-01 | P0 | FR-001-B | Validate a shared receipt fixture | Receipt contains target, check, status, expected/observed, timestamp, evidence, reason, remediation | Checker output + fixture | OPEN | Add or correct receipt schema validation |
| B-TDD-02 | P1 | FR-004-B | Run shared checker against healthy, stale, malformed, mismatch, CORS, and unavailable fixtures | Each fixture produces the documented result and remediation | Fixture matrix output | OPEN | Fix checker taxonomy or contract |
| B-TDD-03 | P1 | FR-008-B | Run `merit-hygiene` against docs/IAR links and near-3 surface | Missing, stale, conflicting, or over-budget docs fail the gate | Hygiene report | OPEN | Repair docs/index/IAR hygiene |
| B-TDD-04 | P2 | FR-009-B | Inventory retained skills and callers | Overlap is documented; consolidation/deprecation has migration notes before change | Skill inventory + caller map | OPEN | Consolidate only proven duplicates |
| B-TDD-05 | P1 | FR-010-B | Validate reusable usage/design/IAR templates | Templates identify owner, evidence location, acceptance IDs, and handoff rules | Template review | OPEN | Update skill templates |
| B-TDD-06 | P1 | FR-011-B | Run repeatable seed-to-readiness procedure | A fresh consumer can reproduce the same checks and receipts | Seed run receipt | OPEN | Fix Hub/skills repeatability |
| B-TDD-07 | P1 | FR-011-B | Run `merit.ps1 e2e --path <repo>` from the public skills checkout | CLI exposes the documented consumer E2E gate, or documentation is corrected to the actual supported command | CLI output + issue/implementation receipt | PASS | — |
| B-TDD-08 | P0 | FR-NEXTREL-002 | Run the standalone Hub from Windows PowerShell 5.1 with no `pwsh` on PATH | Script parses, offers confirmed portable pwsh installation, and relaunches the same Hub after installation | Hub transcript + install path + version output | OPEN | Validate encoding-safe script and bootstrap prompt on a clean Windows device |
| B-TDD-09 | P0 | FR-NEXTREL-002 | Run `Merit-Hub.sh` on Linux/macOS with no `pwsh` | Launcher detects absence, asks for confirmation, installs pinned portable pwsh, and relaunches; declining gives a clear next command | Shell transcript + install path + version output | OPEN | Validate clean POSIX device and package/network failure paths |
| B-TDD-10 | P0 | FR-NEXTREL-003 | Run `scripts/test-merit-law.ps1`, `merit.ps1 law closeout`, and `merit.ps1 closeout --path <repo>` | Contract and law tests pass; binding law prints; closeout writes a receipt; release remains explicit | Test output + closeout-validation.json | PASS | — |
| B-TDD-11 | P0 | FR-NEXTREL-004 | Run `merit.ps1 admin repair-ownership --path <repo>` on an exact Windows Git worktree | Confirmation/UAC, ownership/Modify repair, and write probe succeed; root/non-Git targets are rejected | Admin command transcript + ACL/write probe | OPEN | Validate on a normal elevated Windows device; Codex sandbox UAC is unavailable |

## Zone C — merit-demo consumer

| ID | Pri | FR | Check / command | Expected result | Evidence | Status | Remediation |
|---|---|---|---|---|---|---|---|
| C-TDD-01 | P0 | FR-013-C | `merit.ps1 verify --path C:\DApps\merit-demo` | Public MERIT scaffold verification passes | CLI output | PASS | — |
| C-TDD-02 | P0 | FR-011-C | `merit.ps1 closeout --path C:\DApps\merit-demo` plus `npm run e2e` | Public closeout passes and implementation smoke checks pass | CLI + npm output | PASS | — |
| C-TDD-03 | P0 | FR-012-C | `merit.ps1 e2e:playwright --path C:\DApps\merit-demo` with approved browser | Hello provider ready, Hosted Ready state, mounted workbench, and Register link are present | Playwright output/screenshots | OPEN | Resolve Windows EPERM writing existing evidence screenshots; direct Edge browser assertion previously passed |
| C-TDD-04 | P0 | FR-004-C | Compare `cfg/par_pins.json` to loaded artifact URL and SRI | Configured version, URL, and SRI match the published artifact | Config and browser/network evidence | PASS | Update pin and SRI together |
| C-TDD-05 | P0 | FR-005-C | Block or delay provider initialization | UI leaves Checking and enters labeled Demo Fallback or Runtime Unavailable; no endless spinner | Failure-fixture screenshot/output | OPEN | Add deterministic failure injection and assertions |
| C-TDD-06 | P0 | FR-006-C | Run with CDN/module/network failure | Offline stub shows reason, retry action, and portal/status link | Failure-fixture evidence | OPEN | Harden fallback state |
| C-TDD-07 | P1 | FR-004-C | Serve a version-mismatch fixture | Hosted Ready is rejected and mismatch is visible | Fixture output | OPEN | Add mismatch fixture |
| C-TDD-08 | P1 | FR-005-C | Serve a CORS-denied fixture | Retryable fallback appears and no false Hosted Ready claim is made | Fixture output | OPEN | Add CORS fixture |
| C-TDD-09 | P1 | FR-011-C | Run desktop and mobile route checks | Portal, play, journal, and AMA render at both viewports | Screenshots | PASS | — |
| C-TDD-10 | P1 | FR-007-C | Inspect every non-ready state | Portal link is available in fallback and unavailable states | State screenshots/DOM assertions | OPEN | Add portal link to all failure states |
| C-TDD-11 | P2 | FR-013-C | Compare `dist` against source packaging | CSS, portal, config, and runtime assets are present in `dist` | Build manifest | PASS | — |

## Zone D — merit-prod and here.now cloud plane

| ID | Pri | FR | Check / command | Expected result | Evidence | Status | Remediation |
|---|---|---|---|---|---|---|---|
| D-TDD-01 | P0 | FR-001-D | `GET https://merit-prod.vercel.app/api/health` | HTTP 200 and valid health JSON | Response capture | PASS | Investigate outage or schema |
| D-TDD-02 | P1 | FR-003-D | Inspect health metadata | Service, deployment identity/build SHA, and deployed timestamp are present or explicitly documented unavailable | JSON capture + IAR note | OPEN | Additive metadata contract |
| D-TDD-03 | P0 | FR-003-D | Fetch registry and configured workbench artifact | Registry is reachable and configured `0.4.14` artifact URL/SRI are valid | Registry/artifact capture | PASS | Reconcile registry and consumer pin |
| D-TDD-04 | P1 | FR-004-D | Send approved consumer-origin request | CORS allows the consumer origin and rejects/limits unintended origins | Response headers | OPEN | Configure approved origins |
| D-TDD-05 | P1 | FR-012-D | Check register and meritsubs health routes | Hosted routes respond with expected status/schema | Response capture | PASS | Repair route or contract |
| D-TDD-06 | P1 | FR-013-D | Inspect cache headers and repeat health/registry requests | Health and registry metadata are not stale beyond the documented policy | Header capture | OPEN | Add no-cache/version policy |
| D-TDD-07 | P0 | FR-007-D | Resolve and `GET` the actual here.now portal URL | Published portal is reachable independently of Vercel | URL + response capture | OPEN | Publish or record the real URL |
| D-TDD-08 | P1 | FR-006-D | Test portal while Vercel runtime checks are unavailable | Portal remains reachable and usable without merit-prod | Outage test evidence | OPEN | Remove runtime dependency from portal |
| D-TDD-09 | P1 | FR-007-D | Inspect published source boundary | here.now deployment contains only `portal/` marketing content | Publish receipt/manifest | OPEN | Correct publish scope |
| D-TDD-10 | P1 | FR-007-C | Follow portal links from fallback/unavailable UI | Link resolves to the recorded here.now URL | Browser evidence | OPEN | Wire configured portal URL |

## Cross-zone dependencies

| Dependency | Required ordering |
|---|---|
| A → B | Hub must resolve the skills host before skill receipts can be trusted |
| B → C | Shared pin/checker and hygiene contracts must be available to validate the consumer |
| C → D | Consumer failure states and pin gates must be tested before cloud changes are declared compatible |
| D → C | Cloud metadata, CORS, and portal URL must be fed back into consumer configuration |
| A/B/C/D → closeout | All P0 rows pass; every non-P0 row has PASS or approved disposition; evidence is linked |

## Evidence index

Store evidence under `merit-demo docs/IAR/evidence/` using stable names such as:

- `A-TDD-01-hub-receipt.txt`
- `B-TDD-02-checker-fixtures.json`
- `C-TDD-03-playwright-hosted-ready.txt`
- `C-TDD-06-fallback-network-failure.png`
- `D-TDD-01-vercel-health.json`
- `D-TDD-07-here-now-availability.txt`

Do not claim a cloud or portal result from an agent/sandbox failure. Record the exact URL, timestamp, HTTP status, response headers, and command used.

## Known tool limitation

The bundled Playwright Chromium executable may fail on Windows with `spawn EPERM`. This does not invalidate the application test if the same test passes with an approved installed browser such as Edge. The limitation itself remains a closeout item until the official wrapper completes reliably or the documented Edge path is made the supported runner.

## Final closeout gate

Closeout is permitted only when:

- `npm run verify` passes;
- smoke E2E passes;
- browser E2E passes with recorded executable and evidence;
- Zone D cloud and portal checks are recorded;
- every P0 row is `PASS`;
- every P1/P2 row is `PASS` or has an approved disposition;
- the controlling IAR links this checklist and the evidence index.
