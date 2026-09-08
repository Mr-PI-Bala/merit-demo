# MERIT Demo Ecosystem Plan (SSOT)

**Status:** Plan / controlling IAR until implementation  
**Repo path:** `merit-demo docs/IAR/MERIT_DEMO_ECOSYSTEM_PLAN.md`  
**Updated:** 2026-09-08 (Gaps to Alpha review, TDD and two-repo OC requirements)
**Sources:** Cursor alignment plan + Codex “MERIT Demo Cloud-Recovery IAR” (planning artifact only)

This file is the living SSOT for what to change where. Do **not** invent a parallel `docs/` tree; product docs stay under `merit-demo docs/` (near-3). Cloud report and recovery evidence live **in IAR**, not as a fifth product doc.

**Approval boundary:** This IAR does **not** approve skill deletion/consolidation, runtime changes, portal publication, or deployment. Implementation starts only after explicit execute approval; default first action remains read-only inventory, then Pass 1 (C).

---

## Goal

Make `merit-demo` the reference MERIT consumer:

1. Hub-seeded laptop repos align Cursor / `MYMERITAPP` / `oss-bench` and verify the right skills guidance (IDE skills host).
2. Consumer uses a pinned, verifiable `merit-prod` CompatSet runtime (Hello + DualRail / workbench mount).
3. Hosted failure yields diagnosable states and a **labeled** local fallback—never an endless spinner.
4. `portal/` publishes independently to here.now for marketing.
5. Harden/consolidate skills only where overlap is proven (audit first).

`merit-agent-skills` is a **development/validation** dependency, not a browser runtime. `merit-prod` is the hosted runtime plane. `portal/` has no runtime dependency on Vercel.

---

## Current evidence and interpretation

| Observation | Established fact | Not established | State |
|-------------|------------------|-----------------|-------|
| Hub cloned `merit-demo` under live `MYMERITAPP` (`C:\DApps`) | Local consumer seeded | Cursor workspace always matches `demoFolder` | Confirmed seed; IDE root may still be stale |
| Local `play/index.html` opened | Static page launched | Hosted workbench **mounted** | Confirmed launch; mount gap open |
| Page references pinned `merit_workbench@0.4.14` on the canonical package host | Configured pin + CDN attempt | Health metadata and deployment identity are separately bound to the artifact | Pin reconciled to registry-supported release; runtime contract still open |
| “Loading workbench…” | Bootstrap never reached Hosted Ready UI | Root cause was **no mount call**, not proven CDN outage | Cause classified: missing mount (C), not Vercel down |
| Agent shell/sandbox failures | Agent environment limitation | Does **not** prove Vercel/here.now/skills down | Environment only |
| here.now portal URL | — | Published/reachable URL for this seed | Unverified |
| IDE skills under `~/.cursor/skills` | Typical Hub **I** / install.ps1 target | “Repo `.cursor` trees required” | Host ≠ repo folder |

---

## Zones

| Zone | Code | Owns |
|------|------|------|
| Cursor + Hub laptop follow-through | **A** | Seed receipts, IDE open on `demoFolder`, **IDE skills-host** verification, local HTTP run |
| `merit-agent-skills` / Hub scripts & docs | **B** | Shared validation/receipts, skill harden, templates, hygiene gate, path docs |
| `merit-demo` consumer template | **C** | Startup UX, pins, fallback, DualRail/play exemplar, consumer docs/IAR |
| Vercel `merit-prod` + here.now | **D** | Runtime health/version/CORS, OC DualRail hosted play, portal deploy/verify |

```text
A: Hub seed → verify IDE skills host + open Cursor on demoFolder
         ↓
B: skills → shared cloud-readiness receipt + path/law docs
         ↓
C: merit-demo → Checking → Hosted Ready (pinned CDN + mount)
         │                      └─ fail → Demo Fallback / Runtime Unavailable
         ↓
D: merit-prod runtime          here.now marketing (portal/ only)
```

---

## Conflicts still present in Codex v2 (and SSOT decisions)

| Codex v2 claim | Issue | SSOT decision |
|----------------|-------|---------------|
| Paths `merit-demo/docs/…` + product `merit_demo_cloud_report.md` | Wrong folder name; **5th** product doc vs near-3 | Use **`merit-demo docs/`**; cloud report = **IAR section/evidence**, not a product doc |
| FR-002-A / diagram: skills in **`.cursor`** after seed | Implies repo `.cursor`; install is `~/.cursor/skills` + `.merit-surface.json` | Verify **IDE skills host**; optional thin AGENTS pointers only |
| FR-006-C “functional local **interactive** fallback” / “Interactive local demo” | Reads as full offline workbench; fights thin-consumer / no local PAR | **Labeled offline/demo stub** (reason, retry, portal); interactive only within stub policy—not a silent CDN clone |
| Target diagram: Hub → skills in `.cursor` → checker → consumer | Skips Cursor≠`MYMERITAPP` and DualRail/OC | Keep FR-003-A/B open-Cursor + FR-012 DualRail |
| Execution: B harden → D health → C UI | Leaves spinner unfixed while skills/prod change | **C P0 first** against live CDN; then D gaps; then B; then A |
| Health JSON `service: "merit-workbench"` as sole `/api/health` | May collide with existing merit-prod health schema | **Additive/versioned** contract after inspect; do not blindly replace |
| FR-010-C “usage, design, **cloud-report**, recovery-IAR” as four peer docs | Cloud-report as peer of usage/design breaks ≤4 product docs (INDEX+design+usage+OPERATOR already) | Cloud-report content lives in **this IAR** + `IAR/evidence/` |
| Codex as “controlling recovery IAR” if filed only under skills `docs/IAR/` | Consumer SSOT must live in **consumer** repo | **This file** in `merit-demo docs/IAR/` is controlling; skills may keep a pointer, not a second authority |
| Still thin on DualRail / `createAppShell` / “Register free” | OC DualRail gate expects those markers | Keep FR-012-*; Hello alone is insufficient |
| “Interactive fallback must work when D unreachable” | True for **stub**; false if interpreted as hosting workbench locally | Stub must work offline; Hosted Ready requires D |

**No new major conflict themes** beyond the first Codex pass—v2 mainly strengthens evidence hygiene, approval boundary, and skill non-responsibility (those we adopt).

---

## Functional requirements (merged)

| FR | Zone | Pri | Requirement | Depends |
|----|------|-----|-------------|---------|
| FR-001-A | A | P0 | Hub receipts distinguish clone / local launch / configured / verified hosted; NEXT open Cursor on `demoFolder` | FR-001-B |
| FR-001-B | B | P0 | Receipt schema: target, check, status, expected/observed version, timestamp, evidence, reason, remediation | — |
| FR-001-C | C | P0 | Hosted Ready only after pin/health checks **and** browser init **and** shell mount | FR-004-C, FR-012-C |
| FR-001-D | D | P1 | Verifiable health + immutable deployment metadata (additive) | — |
| FR-002-A | A | P0 | Verify MERIT skills on **IDE skills host** (not require full repo `.cursor` trees) | FR-002-B |
| FR-002-B | B | P0 | Harden install/scaffold validation; no new public availability skill | — |
| FR-002-C | C | P1 | Record skill/host versions in IAR evidence | FR-002-A |
| FR-003-A | A | P0 | Open Cursor on `%MYMERITAPP%` / `oss-bench.demoFolder` for Hub-seeded repos | FR-003-B |
| FR-003-B | B | P0 | Hub “Open in Cursor”; optional `merit-bench.code-workspace`; dinner docs `%MYMERITAPP%` + **skills-v0.5.66** | — |
| FR-003-C | C | P0 | One config surface: runtime URL, `par_pins`, health URL, portal URL, metered bases | FR-003-D |
| FR-003-D | D | P1 | Public no-cache health/metadata usable by B/C (shape finalized after inventory) | — |
| FR-004-B | B | P1 | Shared checker; `merit-deploy-vercel` validates schema/status/freshness/version/CORS/assets/browser readiness | FR-003-D |
| FR-004-C | C | P0 | Import hosted workbench only when observed version **===** configured pin | FR-004-D |
| FR-004-D | D | P1 | Publish real workbench version metadata; approved consumer origins / CORS | — |
| FR-005-C | C | P0 | Checking / Hosted Ready / Demo Fallback / Runtime Unavailable (no spinner loop) | FR-005-D |
| FR-005-D | D | P1 | Failure taxonomy: non-200, malformed metadata, mismatch, CORS, asset, init | — |
| FR-006-C | C | P0 | **Labeled offline/demo stub**: reason, retry, portal link; works if D unreachable | FR-006-D |
| FR-006-D | D | P1 | here.now has no build/runtime dependency on merit-prod | — |
| FR-007-B | B | P1 | Harden `merit-portal` publish + independent verify | FR-004-B |
| FR-007-C | C | P1 | Marketing source `portal/`; link from all non-ready states | FR-007-D |
| FR-007-D | D | P1 | Publish only `portal/` to here.now; verify while Vercel down | — |
| FR-008-B | B | P1 | `merit-hygiene` aggregates install/Vercel/portal/docs/IAR; blocks absent/stale/conflicting | FR-001-B |
| FR-008-C | C | P0 | Claims link to IAR evidence; no unverified Hosted Ready in prose | FR-008-B |
| FR-008-D | D | P2 | Retain Vercel + here.now release URLs/timestamps | — |
| FR-009-B | B | P2 | Skill overlap audit; merge only proven duplicates; migration note before any deprecation | — |
| FR-009-C | C | P2 | Document only retained skills after B audit | FR-009-B |
| FR-010-B | B | P1 | Reusable usage/design/**IAR** templates (not a forced cloud-report product doc) | — |
| FR-010-C | C | P0 | Maintain usage, design, **this IAR** (+ evidence); cloud-report content ⊆ IAR | — |
| FR-011-A | A | P0 | Validate via local HTTP; `file://` smoke-only | FR-011-C |
| FR-011-B | B | P1 | Repeatable seed→cloud readiness via retained skills + hygiene | FR-004-B |
| FR-011-C | C | P0 | Test hosted/retry/fallback/unavailable from served origin | FR-005-C |
| FR-011-D | D | P2 | Healthy/unhealthy/mismatch/CORS fixtures + portal-up-while-down | — |
| FR-012-C | C | P0 | DualRail / `createAppShell` + mount after Hello; e2e asserts mount / “Register free” as needed | FR-012-B/D |
| FR-012-B | B | P1 | `par scaffold` matches OC DualRail expectations | — |
| FR-012-D | D | P1 | OC hosted play DualRail-compatible with C exemplar | — |
| FR-013-C | C | P1 | Honest `par_pins`/SOTU/HTML; `build.mjs` copies CSS/portal for dist | — |
| FR-013-D | D | P2 | Document CompatSet **baseline pin** vs registry latest; lock pin after inventory | FR-013-C |

---

## Retained skills (with non-responsibility)

| Skill | Retain | Responsibility | Explicit non-responsibility |
|-------|--------|----------------|----------------------------|
| `merit-deploy-vercel` | Yes | Deploy + health/version/CORS/asset/browser readiness via shared checker | Marketing publish; consumer UI implementation |
| `merit-portal` | Yes | here.now publish + independent availability evidence | Vercel runtime verification |
| `merit-hygiene` | Yes | Aggregate receipts; docs/IAR gate; fail incomplete evidence | Owning duplicate low-level HTTP/version probes (uses shared checker) |
| `merit-surface` | Yes | Discover surfaces / `where`; tip open `demoFolder` | Deployment behavior |
| `merit-par-workbench` | Yes | DualRail Gloss scaffold aligned with FR-012 | Becoming the runtime CDN |
| Shared internal checker | Yes (internal) | Normalized availability/compatibility checks | New public-facing skill |
| New availability skill | **No** | — | Skill proliferation |

No deprecation before read-only catalog audit + caller map + migration note.

---

## Runtime contract (proposed; lock after inventory)

Public, `Cache-Control: no-store`. Field names/additive merge remain subject to live `/api/health` inspection. `0.4.14` is the **registry-supported consumer pin**; asset provenance and health metadata still require binding evidence.

```json
{
  "status": "ok",
  "service": "merit-prod",
  "workbenchVersion": "0.4.14",
  "deploymentId": "immutable-deployment-id",
  "buildSha": "source-revision",
  "deployedAt": "ISO-8601 timestamp"
}
```

Consumer Hosted Ready requires observed workbench artifact version **===** `cfg/par_pins.json` (and health metadata when present).

---

## Consumer UI states

| State | Trigger | Required behavior |
|-------|---------|-------------------|
| Checking | Bootstrap | Neutral progress; no success claim |
| Hosted Ready | Health/pin/asset/init **+ mount** | Interactive hosted shell; show verified version/host |
| Demo Fallback | Network/CORS/module/init/mismatch | **Labeled offline stub**; reason, retry, portal link |
| Runtime Unavailable | Stub cannot init | Clear error; retry; portal/status |

---

## Documentation map (near-3)

| Artifact | Role |
|----------|------|
| `merit-demo docs/INDEX.md` | Nav |
| `merit-demo docs/merit_demo_usage.md` | Setup, HTTP, states, troubleshooting |
| `merit-demo docs/merit_demo_design.md` | Planes, boundaries, version policy, ownership |
| `merit-demo docs/OPERATOR_PROVISION.md` | Ops checklist (4th product doc) |
| **`merit-demo docs/IAR/MERIT_DEMO_ECOSYSTEM_PLAN.md`** | **This controlling SSOT** |
| `merit-demo docs/IAR/SOTU.md` + `evidence/` | Status + screenshots/receipts (includes cloud-report tables) |
| `merit-demo docs/IAR/MERIT_DEMO_TDD_CHECKLIST.md` | Executable Zone A/B/C/D test checklist and closeout gate |

---

## Test and release gates

The executable test authority is [MERIT_DEMO_TDD_CHECKLIST.md](MERIT_DEMO_TDD_CHECKLIST.md). The matrix below is the scenario summary; the checklist contains the row-level command, expected result, evidence, and status.

| Scenario | Expected | FRs |
|----------|----------|-----|
| Fresh Hub seed | IDE skills host verified; receipt truthful; Cursor can open `demoFolder` | FR-001-A, FR-002-A, FR-003-A |
| Healthy compatible runtime | Pin match; Hello + mounted shell; Hosted Ready | FR-003-D, FR-004-C, FR-012-C |
| Vercel outage | Stub works; portal reachable | FR-005-C, FR-006-C, FR-007-D |
| Version mismatch | Hosted rejected; clear fallback | FR-004-B, FR-004-C |
| CORS/asset failure | No spinner; retry + fallback | FR-004-D, FR-005-C |
| Portal independence | here.now up while Vercel down | FR-006-D, FR-007-D |
| Missing/stale receipt | Hygiene blocks release | FR-008-B |
| Skill audit | Inventory maps consolidations | FR-009-B |

---

## Implementation sequence

1. Read-only inventory (demo, IDE skills host, skills catalog, live health/registry, portal).  
2. **Pass 1 — C P0:** states + mount + HTTP + pin gate + IAR evidence hooks.  
3. **Pass 2 — D gaps:** health/metadata/CORS only where inspect shows missing.  
4. **Pass 3 — B:** receipts, shared checker, dinner/path docs, Hub open-Cursor, hygiene.  
5. **Pass 4 — A:** Cursor workspace habit + verification receipts.  
6. Portal independent publish/verify.  
7. Hygiene gate + closeout evidence in IAR.

---

## Status

### Documentation presentation standard

MERIT documentation follows the shared format standard in
[`merit-agent-skills` LLD map](https://github.com/AgentDraven/merit-agent-skills/blob/main/docs/IAR/MERIT_AGENT_SKILLS_LLD_MAP.md#documentation-format-standard): colored bands for major sections, normal Markdown subheadings, callout blockquotes, command-first examples, and tables for matrices. This IAR remains the controlling content authority; styling must not create parallel documents.

### NextRel FR — host-compatible closeout enforcement

2026-09-06 evidence: skills-repo ownership status is clean (`AgentCreator\\Draven`, Modify ACL, write probe PASS, git safe-directory PASS). The prior closeout receipt used deterministic temp storage because the target evidence directory was unavailable or unwritable in that execution context; this is an evidence-path issue, not a root ownership failure.

The detailed cross-harness implementation, host matrix, hook gotchas, receipts, and verification gate are maintained in the skills-plane IAR: [MERIT_CLOSEOUT_ENFORCEMENT.iar.md](../../../merit-agent-skills/docs/IAR/MERIT_CLOSEOUT_ENFORCEMENT.iar.md). The executable validation worksheet is [MERIT_CLOSEOUT_ENFORCEMENT_CHECKLIST.md](../../../merit-agent-skills/docs/IAR/MERIT_CLOSEOUT_ENFORCEMENT_CHECKLIST.md). MERIT skills are development/validation guidance; hooks are optional adapters; this consumer must never claim universal post-chat enforcement. Consumer closeout remains governed by the installed contract and `merit.ps1 closeout`; cloud/runtime behavior is independent of AI-harness lifecycle enforcement.

`FR-NEXTREL-005-B` requires installation to make the enforcement boundary explicit. Cursor receives the MERIT `stop` hook, which injects the closeout law and 3-3 reminder before an agent turn ends. Hosts without a supported post-turn hook receive `.merit-hook-warning.json` and the same persistent skill guidance; they are **not** claimed to be forcibly enforced. All hosts remain release-gated by a valid `closeout-validation.json` before `ship`. Exceptions are explicit: WIP, local-only, and no-commit.

| Host / harness | Hook enforcement | Installer result | Remaining control |
| --- | --- | --- | --- |
| Cursor | **Supported** (`stop`) | Installs/merges `~/.cursor/hooks.json` and `~/.cursor/hooks/merit-closeout-stop.ps1` | User may disable hooks; release receipt still gates `ship` |
| ClaudeCode | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| Codex | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| VSCode / Agents | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| Hermes, OpenClaw, GrokBot, Devin | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| Project target | Project skills only; no host event assumed | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |

This does **not** prove that every AI IDE or harness enforces 3-3 after every chat. It provides one deterministic adapter where supported, transparent warnings everywhere else, and a machine-enforced release boundary.

### NextRel FR — host-compatible closeout enforcement

`FR-NEXTREL-005-B` requires installation to make the enforcement boundary explicit. Cursor receives the MERIT `stop` hook, which injects the closeout law and 3-3 reminder before an agent turn ends. Hosts without a supported post-turn hook receive `.merit-hook-warning.json` and the same persistent skill guidance; they are **not** claimed to be forcibly enforced. All hosts remain release-gated by a valid `closeout-validation.json` before `ship`. Exceptions are explicit: WIP, local-only, and no-commit.

| Host / harness | Hook enforcement | Installer result | Remaining control |
| --- | --- | --- | --- |
| Cursor | **Supported** (`stop`) | Installs/merges `~/.cursor/hooks.json` and `~/.cursor/hooks/merit-closeout-stop.ps1` | User may disable hooks; release receipt still gates `ship` |
| ClaudeCode | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| Codex | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| VSCode / Agents | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| Hermes, OpenClaw, GrokBot, Devin | Not verified/supported by this installer | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |
| Project target | Project skills only; no host event assumed | Warning receipt + skills guidance | Agent compliance + closeout/ship gate |

This does **not** prove that every AI IDE or harness enforces 3-3 after every chat. It provides one deterministic adapter where supported, transparent warnings everywhere else, and a machine-enforced release boundary.

| FR | Status | Evidence |
|----|--------|----------|
| FR-005-C, FR-006-C, FR-012-C, FR-001-C, FR-003-C, FR-004-C (page pin), FR-011-C | **DONE (Pass 1)** | Playwright: Hosted Ready + mount + Register free; smoke e2e OK; `play/index.html` DualRail states |
| FR-010-C | **PARTIAL** | This IAR + refreshed usage/design/AGENTS/README |
| All other FRs | **PLANNED** | Awaiting Pass 2–4 |

## NextRel FR register

### FR-NEXTREL-006 — IAR consolidation and vault handoff

Keep IAR documentation to a small, role-based set. New requirements belong in the controlling IAR, executable checks in the existing checklist, and historical proof in evidence packets. A new IAR file or subfolder requires written rationale and a README. When `merit-private-vault` and `MERIT.instructions` are activated, port the policy, contract, checklist, and consolidation rules as one vault package without creating a parallel consumer authority.

| Zone | Owner | Acceptance |
|---|---|---|
| B | `merit-agent-skills` | IAR README exists; active files have declared roles; duplicate authorities are removed or explicitly marked historical |
| C | `merit-demo` | Consumer IAR links skills policy/checklist and does not duplicate host policy |
| D | `merit-private-vault` / `MERIT.instructions` | Vault upgrade preserves one controlling authority and adds protected evidence only where necessary |

### FR-NEXTREL-007 — Release closeout must reach the cloud

Validation-only closeout is not release completion. The canonical release path is `merit.ps1 closeout --path <repo> --release` (or `merit.ps1 release --path <repo>`): validate, commit, and push the current branch. Skills repositories additionally run `merit.ps1 ship` to create/push the `skills-v*` tag. Hooks and installers must use validation-only mode unless the user explicitly requests release. A release is incomplete if the push fails; local commits alone do not satisfy closeout.

| NextRel FR | Zone | Requirement | Port target | Acceptance evidence |
|---|---|---|---|---|
| FR-NEXTREL-001 | B | Public `merit.ps1 e2e --path <repo>` and `merit.ps1 e2e:playwright --path <repo>` must run the consumer's declared checks with exit-code propagation and clear diagnostics. | Port the implementation from OSS `merit-agent-skills/merit.ps1` into the master `merit.ps1` in `merit-private-vault` when that repo is activated. | Static wrapper passes; browser wrapper dispatches but is currently blocked by Windows EPERM writing existing evidence screenshots; missing package/script and non-zero child exit handling is implemented; private-vault parity test remains pending. |
| FR-NEXTREL-002 | B | Merit-Hub must be usable on a fresh device without assuming `pwsh`: Windows PowerShell 5.1 must parse the standalone Hub, offer confirmed laptop-local pwsh installation, and relaunch; `Merit-Hub.sh` must detect missing pwsh on Linux/macOS, request confirmation, install a pinned portable build, and relaunch the same Hub. | Port the launcher/bootstrap behavior into the master Hub implementation in `merit-private-vault` when that repo is activated. | Windows 5.1 parse smoke, confirmed portable install/relaunch, POSIX missing-pwsh confirmation path, declined-install diagnostic, and new-device clone/seed receipt. |
| FR-NEXTREL-003 | B | MERIT closeout law must be machine-readable and install-enforced: installation emits a law receipt, validation emits a closeout receipt, release refuses stale/missing validation, and every completed scope requires the 3-3 response. | Port `cfg/merit_closeout_contract.json`, install receipt, closeout receipt, safe-directory handling, and release gate into the future `merit-private-vault` master CLI. | `scripts/test-merit-law.ps1` passes; `merit.ps1 law closeout` prints the binding sequence; `merit.ps1 closeout` writes receipt; `ship` requires a recent receipt; no automatic commit/push occurs during install or validation. |
| FR-NEXTREL-004 | B | Add `merit.ps1 admin repair-ownership --path <repo>` as a scoped Windows recovery task for exact Git worktrees whose ACL/owner blocks evidence or Git operations. | Port the admin recovery command into the future `merit-private-vault` master CLI and keep Hub/skills guidance aligned. | Exact-path guard, confirmation/UAC, `takeown`, current-user Modify grant, write probe, and refusal of filesystem roots/non-Git paths. |

## Evidence and result storage

| Result | Stored location / review method |
|---|---|
| Zone checklist and statuses | `merit-demo docs/IAR/MERIT_DEMO_TDD_CHECKLIST.md` |
| Controlling requirements and NextRel FRs | This IAR |
| Browser screenshots | `merit-demo docs/evidence/` |
| CLI test output | Capture with `Tee-Object` into `merit-demo docs/IAR/evidence/`; CLI commands do not persist text output automatically |
| Cloud response evidence | `merit-demo docs/IAR/evidence/` with URL, timestamp, status, headers, and response body |

The browser screenshot set currently contains prior desktop/mobile route evidence. The latest `merit.ps1 e2e:playwright` attempt dispatched correctly but remained open because Windows returned `EPERM` while overwriting an existing screenshot; this must not be recorded as a fresh browser pass.

Pass 1 verify: `.\merit.ps1 verify` / `.\merit.ps1 e2e` / `.\merit.ps1 closeout`. Browse with `.\merit.ps1 serve` → http://localhost:3000/play/ → `data-runtime-state="hosted-ready"`.


---

## Changelog — Codex cloud-recovery IAR review log

What we **took in**, **adapted**, or **did not take**, and why.

### Took in (as-is or nearly as-is)

- Four-zone model A/B/C/D with separately accountable FR rows per zone.
- UI state machine: Checking / Hosted Ready / Demo Fallback / Runtime Unavailable.
- Normalized validation **receipt** fields (target, check, status, expected/observed, timestamp, evidence, reason, remediation).
- Exact **version pin match** before Hosted Ready.
- One **internal** shared cloud-readiness checker; **no** new public availability skill.
- Harden retained skills: `merit-deploy-vercel`, `merit-portal`, `merit-hygiene`; keep `merit-surface` for discovery.
- Skill **non-responsibility** column and “no deprecation before audit + migration note.”
- here.now **independent** of Vercel; publish `portal/` only; verify during intentional outage.
- `file://` = smoke-only; real validation over **local HTTP**.
- IAR as controlling evidence; prose must not claim unverified cloud readiness.
- **Approval boundary**: writing the IAR ≠ approving deletes/deploys.
- Evidence hygiene: agent/shell failures ≠ proof that Vercel/skills/portal are down.
- Pin reconciliation: registry inventory identified `0.4.9`, `0.4.10`, and `0.4.14`; consumer pin, canonical URL, and SRI now align to supported `0.4.14`.
- Test/release gate matrix linking scenarios → FRs.
- Clarification: skills = build/validate plane; merit-prod = browser runtime plane.

### Adapted (kept intent, changed shape)

- **Doc paths:** Codex `merit-demo/docs/` → **`merit-demo docs/`** (actual near-3 surface).
- **Cloud report:** Codex product `merit_demo_cloud_report.md` → **IAR sections + `IAR/evidence/`** (avoid 5th product doc; INDEX+design+usage+OPERATOR already fill the budget).
- **FR-002 `.cursor`:** Codex “skills in `.cursor`” → verify **`~/.cursor/skills` / IDE skills host** + surface pointer; consumer may document, not vendor full skill trees.
- **FR-006 fallback:** Codex “interactive local demo / functional interactive fallback” → **labeled offline/demo stub** (reason, retry, portal); must work when D is down without bundling a second workbench CDN.
- **Health contract:** Codex sole new `/api/health` shape with `service: merit-workbench` → **additive/versioned** metadata after inspect; prefer `service: merit-prod` (or preserve existing fields).
- **Execution order:** Codex B→D→C → SSOT **inventory → C P0 → D gaps → B → A** so the spinner/exemplar is fixed against today’s CDN.
- **FR-001-C Hosted Ready:** Codex “verified receipt + init” → also require **shell mount** (FR-012), not Hello/`data-provider-ready` alone.
- **FR-010 templates:** Codex “usage, design, cloud-report, IAR” blobs → reusable **usage/design/IAR** templates; cloud-report is an IAR evidence pattern, not a forced fourth consumer markdown product.
- **Controlling IAR location:** Codex recovery IAR under skills (or generic docs) → **this consumer file** is SSOT; skills may point here, not fork authority.
- **Diagram Hub→`.cursor`:** redrawn as Hub→**IDE skills host** + open **`demoFolder`**.

### Did not take (rejected) — and why

- **New product doc `merit_demo_cloud_report.md`** — fails near-3 / hygiene (would be a 5th top-level product doc alongside OPERATOR_PROVISION).
- **Renaming/moving to `docs/`** — would break existing AGENTS/INDEX and invent a parallel tree.
- **Requiring full MERIT skill packs inside repo `.cursor`** — contradicts Hub `install.ps1 -Target Cursor` (user skills host); duplicates and drifts from skills pin.
- **Silent full offline workbench / local PAR clone as default fallback** — violates public thin-consumer boundary (no local metered/PAR provider source; no billing bypass lookalike).
- **Replacing live `/api/health` without inventory** — risk breaking existing e2e/consumers; must extend after inspect.
- **Skills+Vercel-first implementation sequence as the only path** — delays the user-visible spinner fix that is entirely C-local.
- **Treating Hello World CDN presence as Hosted Ready** — OC DualRail / exemplar needs mount + `createAppShell` / Register markers (FR-012).
- **Dropping Cursor≠`MYMERITAPP` / open-`demoFolder` work** — Codex v2 still under-specifies this; Hub already sets env, Cursor does not follow automatically.
- **Dropping DualRail / `par scaffold` / OC gate alignment** — still required for cloud-matched exemplar.
- **Making Codex’s copy in `merit-agent-skills/docs/IAR/` a second controlling SSOT** — one authority: this consumer IAR file.
- **Claiming implementation or deployment in the plan** — both Codex and SSOT remain planning-only until execute approval.

### Still open (not conflicts — work remaining)

- Live inspect/bind of merit-prod health schema, CORS, and immutable artifact provenance.
- Official Playwright closeout on the generated `dist` artifact using the configurable Edge executable; bundled Chromium remains `spawn EPERM` on this Windows host.
- Published here.now URL for this seed (unverified).
- Whether a future **law-approved** optional vendored read-only PAR is ever allowed for richer offline demo (explicitly out of Pass 1).
- Pass 2–4 ownership when writing to skills Hub / merit-prod (may be hand-off).

---

<a id="gaps-to-alpha"></a>

## Gaps to Alpha ^gaps-to-alpha

**Review date:** 2026-09-08. **Status:** OPEN requirements; guided builder preview candidate, not subscriber-alpha signoff. **Authority:** this controlling consumer IAR. This section records the three-repo review and the owner's request to define fixes, acceptance tests, personas, and two-repo OC independence. Documentation approval does not claim implementation, provider ACCEPT, deployment, or a passing alpha gate.

### Product boundary: OC needs only the two public repos

OC (OSS in Cloud) must be installable, runnable, diagnosable, and verifiable using **merit-agent-skills + merit-demo only** as local source repositories. A normal user must not clone merit-private-vault, deploy an affiliate runtime, run its operator CLI, or obtain private operator/gateway/provider secrets. IDE skills are optional; a specific IDE is not a runtime prerequisite. Publicly documented prerequisites may be installed by the public Hub with an explicit explanation.

This is a local-repository independence requirement, not an offline promise: hosted merit-prod, meritutils packages, meritsubs, and meritstore remain service dependencies. Standard platform OC must not require local provider source, personal Vercel/Square/Supabase credentials, or a here.now account. BYOK/own-host publication is a separately labeled Advanced pathway, never a silent prerequisite. Platform subscriber/builder identity may be required and must be explained before use.

Ownership remains: **A** = Hub/laptop/optional IDE follow-through; **B** = public skills/CLI; **C** = merit-demo consumer; **D** = hosted providers and marketing hosting. Vault owns private policy and operator controls, not public consumer implementation. Any future vault feature is recorded here as a requester-owned **NextRel FR for later extraction**, with no current vault edits and no dependency from the standard OC path to that future work. Cross-repo handoffs stay in IAR; these are not same-repo maintenance-line NextRelDoc packets.

### Review baseline and evidence limits

| Surface | Observed on 2026-09-08 | Interpretation |
|---|---|---|
| merit-agent-skills | VERSION 0.5.193; HEAD eba7094; four commits after skills-v0.5.193 | Public tooling exists; release payload must include the intended fixes before alpha |
| merit-demo | VERSION 0.3.15; HEAD c47c8bf; eight commits after v0.3.15; package.json 0.3.10 | Thin consumer exists; version surfaces and tested release need reconciliation |
| merit-private-vault | vault-v0.5.56 at 98f3228 | Private operator plane exists; not a required subscriber checkout |
| Fresh checks | Hub launcher regression suite and demo scaffold verification passed; gateway health, meritsubs health, workbench 0.4.14 JS returned 200 | Infrastructure/scaffold evidence only; no complete registration/payment/browser acceptance test was run |
| Register free | /store/merit-demo/register resolved to /portal/developers/sku-commerce/ with final 200 | Guidance for store activation, not completed registration; must not pass subscriber acceptance |
| Vault unit checks | Selected tests could not run: available Python lacked pytest | Environment limitation, not a demonstrated test failure or a PASS |
| Earlier IAR evidence | Previous release, commerce, and browser results exist | Historical evidence does not certify the current selected release |

Source pointers: [demo API calls and fallback](../../journal/index.html), [AMA rendering and calls](../../ama/index.html), [browser gate](../../scripts/e2e-playwright.mjs), [version manifest](../../package.json), [consumer service boundary](../../cfg/meritsubs_consumer.json). Public tooling source: merit-agent-skills README release section, Merit-Hub embedded skillsPin, cfg/compatset.skills.json, scripts/test-hub-launcher.ps1. Review statements are observations or risks; no production exploit, charge, or signup was attempted.

### Bugs to fix

All rows begin **OPEN**. P0 blocks free subscriber alpha; P1 blocks alpha for the affected advertised pathway. Severity expresses release priority, not a confirmed exploit assessment.

| Bug ID | Priority / zone / owner | Defect and required correction | Red test -> green acceptance |
|---|---|---|---|
| BUG-ALPHA-001 | P0 C / demo | Register free promises registration but reaches commerce guidance. Bind the CTA to a live consumer registration route; show an honest unavailable/setup state if activation fails. Provider activation is FR-ALPHA-002-D. | Follow every redirect from play/portal CTA; fail on guide/help/login-wall/unrelated tenant destination; pass only on the intended consumer registration form and successful completion |
| BUG-ALPHA-002 | P0 C / demo | Journal/AMA requests lack explicit consumer context, subscriber authentication, and a visible return-to-app identity bridge. Wire the supported public provider identity contract; never ship server secrets. | Assert context on all read/write/vote calls; guest/free/paid sessions resolve correctly; missing/expired/foreign context is rejected or follows a documented guest path; user B cannot read user A's private journal |
| BUG-ALPHA-003 | P0 C / demo | AMA interpolates API-provided body/identity/id fields into innerHTML. Replace unsafe rendering with text/DOM APIs or an explicitly validated rich-text contract. | Inject hostile markup into all rendered fields in isolated fixtures; no script/event execution or attribute injection; text and voting still work. Do not inject payloads into production |
| BUG-ALPHA-004 | P0 C / demo tests | Browser dependency absence can skip acceptance, and HTTP 200 after a wrong redirect can pass. Required alpha browser/provider checks must fail closed. | Remove browser dependency, return guide HTML or malformed health JSON with 200, redirect to wrong tenant; each must produce a nonzero gate and explicit reason, never E2E OK |
| BUG-ALPHA-005 | P1 C / demo | Journal 503 fallback retains only the last cap entries, conflating retention with daily metering; network errors lack reliable recovery. Preserve accepted entries, identify local-only persistence, and keep provider entitlement enforcement authoritative. | Save more than two local entries under outage; reload without silent loss; exercise network error, 503, malformed JSON, storage failure, retry and duplicate prevention; no false cloud-save claim |
| BUG-ALPHA-006 | P0 B / skills release | Default skills payload omits later fixes and README baseline differs from the selected release. Select/publish a tested pin and align Hub, CompatSet, receipts, and public guidance. | Clean installation resolves the advertised immutable payload containing required fixes; repeated install and supported-host startup tests pass without floating-main evidence being substituted |
| BUG-ALPHA-007 | P0 C / demo release | VERSION, package metadata, tag/commit, and current release evidence disagree. Reconcile version-bearing surfaces and release the exact tested revision. | Check metadata against declared release; receipt binds commit, tag, skills pin, consumer artifact, provider versions and UTC time; published revision matches the tested revision |
| BUG-ALPHA-008 | P1 C / docs | Existing TDD command descriptions call closeout validation-only, while current wrappers can release by default. Correct documentation and distinguish validation, release, and deploy. | Execute the documented validation path in an isolated fixture; no commit/push/deploy; separately verify explicit release behavior and nonzero failure propagation |

### Features required for alpha

All rows are **OPEN / not ACCEPTED**. Separate rows preserve ownership; provider work must be requested and accepted through this IAR, not copied into either public repo.

| FR ID | Gate / zone / owner | Required feature | Acceptance evidence |
|---|---|---|---|
| FR-ALPHA-001-A | Free P0 / A / Hub | Fresh-device two-repo OC journey with correct resolved paths; optional IDE installation; no vault-dependent detours | Clean normal-user profile with no vault/runtime, no private env, no provider source and only the two public checkouts completes Setup -> Install -> Try -> 3V -> OC -> OCV; repeat/resume remains safe |
| FR-ALPHA-001-B | Free P0 / B / skills | Public CLI provides every standard OC action and diagnostic, including activation orchestration and actionable service failures | Integration tests deny reads/exec from vault/runtime and detect attempts; public flow succeeds; installed-vault and no-vault cases produce equivalent public outcomes without selecting private authority |
| FR-ALPHA-001-C | Free P0 / C / demo | Consumer runs and validates with the public tooling alone; correct per-app URLs and identity return route | Two fresh consumer slugs publish/open independently; configuration contains no private secrets or absolute operator paths; subscribers need no checkout or IDE |
| FR-ALPHA-002-B | Free P0 / B / skills | OC activates or reuses the app's free store via supported public service contract, with idempotent retry and visible status | First activation, repeated activation, collision, timeout and resume tests; receipt identifies consumer and final play/register URLs; no raw provider credential prompt |
| FR-ALPHA-002-D | Free P0 / D / merit-prod + meritstore | Real registration for demo and newly created consumers, platform identity, free entitlement and return-to-app flow | Browser completes registration/login/logout/relogin for two apps; duplicate handle/email, verification/recovery and interrupted flow behave as documented; wrong-consumer redirect fails |
| FR-ALPHA-003-D | Free P0 / D / meritsubs + gateway/community providers | Authoritative authenticated tenant/subscriber routing, private-journal isolation, quota decisions and entitlement lookup | API tests with missing/forged/expired identities and two users/two tenants; no cross-tenant/private-user leakage; client-edited tier/cap cannot grant access; identity is verified, not trusted from a submitted ID |
| FR-ALPHA-004-C | Free P0 / C / demo | Visible guest/free/paid state, working save/reload and AMA ask/vote, actionable limit/upgrade and auth recovery UX | Guest -> register -> return -> save/reload; third daily action reaches configured limit; refresh/relogin preserves tier; rejected votes show failure; no invented saved/paid state |
| FR-ALPHA-004-D | Free P0 / D / community providers | Server-side daily quota boundaries, persistence, vote integrity, privacy modes and advertised leaderboard behavior | Clock-controlled reset-boundary tests, concurrent request tests, replay/double-vote policy, privacy projections and top-25 rule; persisted journal survives a new session |
| FR-ALPHA-005-D | Paid P0 / D / meritstore + meritsubs | Paid SKU activation, tokenized checkout, webhook/ledger/entitlement reconciliation, cancellation and refund/revocation | Sandbox/provider-owned payment tests: success, decline, cancel, duplicate/delayed/out-of-order webhook, renewal failure, refund terminal status and entitlement transition; approved production proof separately, with safe identifiers only |
| FR-ALPHA-005-C | Paid P0 / C / demo | Paid entitlement unlock and subsequent downgrade/revocation reflected in the consumer | Same subscriber upgrades and receives configured uncapped access within documented bound; reload/relogin consistent; cancellation/refund semantics match provider policy; payment failure never unlocks |
| FR-ALPHA-006-B | Free P0 / B / skills validation | Required OCV produces trustworthy semantic browser evidence, not status-code-only checks | Gate consumes tests for correct tenant/form, auth, mount, real persistence and quotas; missing tools, stale receipts, skipped required scenarios and provider failure block acceptance |
| FR-ALPHA-006-C | Free P0 / C / demo tests | Executable persona-path acceptance suite mapped to every bug/FR | Red/green fixtures and live dedicated-test-tenant runs; desktop/mobile, keyboard/forms, failure/retry and cross-session checks; no new route-smoke-only claims |
| FR-ALPHA-007-C | Free P0 / C / docs | Document personas/pathways below in existing usage/design docs, including data/privacy, limits, support and recovery | A new tester follows each applicable path without operator interpretation; documented labels, final URLs, side effects and evidence match actual behavior |
| FR-ALPHA-007-D | Free P0 / D / providers | Operational support for alpha: health/version diagnostics, redacted correlation IDs, abuse escalation and documented recovery/rollback | Induced service failure produces actionable trace and support route without secrets/PII; operator rehearses recovery; restore/reconciliation evidence supports advertised persistence |

Paid alpha is a separate gate: do not advertise functioning paid onboarding while FR-ALPHA-005-C/D remain open. Free alpha still requires the complete free identity/data/quota journey. A published marketing page or Hosted Ready workbench alone satisfies neither gate.

### Personas and pathways to document and test

Document each path in the existing merit_demo_usage.md, explaining prerequisites, exact actions/labels, local versus hosted URLs, expected result, data visibility, side effects, failure/retry, support, and evidence. Put architecture/ownership rationale in merit_demo_design.md; keep acceptance status in this IAR and the linked TDD checklist.

| Path ID / persona | Required journey | Key acceptance / traceability |
|---|---|---|
| PATH-ALPHA-01 / first-time builder | Setup (1) -> Install OSS (2) -> Try (3) -> local 3V -> OC -> hosted OCV | Only two repos, supported prerequisites, correct demoFolder, local/hosted distinction, no mandatory IDE/vault/BYOK; FR-ALPHA-001-A/B/C |
| PATH-ALPHA-02 / returning builder | Reopen -> select app -> resume/retry OC -> OCV -> share | Idempotent activation, no duplicate tenant, correct app identity, preserved work and actionable failure receipt; FR-ALPHA-002-B |
| PATH-ALPHA-03 / guest visitor | Shared hosted URL -> workbench -> journal/AMA preview -> Register free | Browser only; honest guest capabilities and limits; real registration destination, no developer guide surprise; BUG-ALPHA-001, FR-ALPHA-004-C |
| PATH-ALPHA-04 / free subscriber | Register -> identity verification if required -> return to app -> save/reload -> ask/vote -> cap -> logout/relogin/recover access | Persistence, verified identity, configured daily reset, clear upgrade and recovery; BUG-ALPHA-002/005, FR-ALPHA-002-D/003-D/004-C/D |
| PATH-ALPHA-05 / paid subscriber | Free account -> choose SKU -> checkout -> return -> paid access -> cancel/refund -> resulting access | Payment/entitlement consistency, failures and delayed webhook handling, accurate billing/cancellation copy; FR-ALPHA-005-C/D |
| PATH-ALPHA-06 / privacy and abuse tester | Two users in two apps -> private journals -> AMA privacy modes -> hostile-content fixtures -> report abuse | Tenant/user isolation, safe rendering, leaderboard privacy, support response path; BUG-ALPHA-003, FR-ALPHA-003-D/004-D/007-D |
| PATH-ALPHA-07 / release and support operator | Select public pins -> run acceptance -> review receipts -> explicit release -> diagnose failure -> rollback/recover | No false-green skips, tested/published revision binding, redacted diagnostics; BUG-ALPHA-004/006/007/008, FR-ALPHA-006-B/C/007-D |
| PATH-ALPHA-08 / advanced BYOK builder | Explicitly choose own hosting/marketing publication -> supply own account -> publish -> verify | Separate optional path, credentials requested only after selection, no regression to standard OC independence; never counted as standard OC prerequisite |

### TDD execution and release decision

1. **Red first:** implement a test for each bug/FR before changing behavior. Record the observed failing assertion; an unimplemented test stays OPEN, an unavailable environment is BLOCKED, and a skipped mandatory test is never PASS. Provider tests run in their owner repo; consumer acceptance links their receipts here.
2. **Unit and contract tests:** safe rendering, fallback retention, release metadata, redirect validation, identity/request composition, activation retries, quota clocks, webhook idempotency and fail-closed receipt checks. Fixtures must test outcomes, not just mirror source strings.
3. **Hermetic integration:** two users x two consumer tenants; providers simulated for controlled negative cases. Block vault/runtime filesystem and CLI access and remove private env; verify public commands neither require nor probe secrets. Test local-vault presence separately so it cannot silently change OC behavior.
4. **Browser acceptance:** clean profile, pinned two-repo release, dedicated hosted test tenants. Exercise PATH-ALPHA-01 through 07 as applicable, desktop/mobile and keyboard flows, real form submission, navigation/redirect destination, return session, persisted data and entitlements. Inject outage/CORS/timeout/malformed response in controlled fixtures; prove recovery without data loss. Do not submit hostile data or charge cards on production as part of ordinary regression.
5. **Public validation entry points:** use public merit.ps1 verify, e2e and e2e:playwright with the resolved consumer path. Validation-only must be explicitly selected and confirmed against the current wrapper; bare closeout can commit/push. Missing mandatory browser/provider test support must block alpha even if today's wrapper exits zero. Release and deployment are separate explicit actions.
6. **Evidence:** under IAR/evidence retain a run manifest with bug/FR/path IDs, owner, UTC timestamp, public repo commits/tags, expected/observed provider versions, local versus hosted origin, consumer/test-user aliases, final redirect URLs, expected/actual assertions, exit status and redacted logs/screenshots. Never retain session tokens, raw credentials, card data or unnecessary subscriber PII. Current release evidence supersedes historical PASS labels for alpha signoff only; preserve history.
7. **Accept:** all Free P0 and advertised-path P1 items pass on the selected released artifacts; paid launch additionally requires both Paid P0 rows. Provider dependencies require requester-IAR ACCEPT linked to provider evidence. Unresolved mandatory bugs, skipped tests, stale/conflicting pins or missing persona evidence mean NO-GO. No percentage readiness score substitutes for these gates.

### NextRel FRs: future extraction by merit-private-vault

All entries are **OPEN / REQUESTED / NOT ACCEPTED / NOT EXTRACTED**. Source is this merit-demo IAR; target is merit-private-vault; owner is its operator maintainer when that repo takes the work. These improve governance later and are **not prerequisites for two-repo OC or substitutes for current public/provider fixes**.

| NextRel FR ID | Future vault feature | Acceptance after extraction / non-goal |
|---|---|---|
| FR-NEXTREL-ALPHA-VAULT-001 | Import alpha evidence by bug/FR/path ID into certification and portfolio state; distinguish historical, blocked, current free-alpha and paid-alpha results | Fixture with stale release, skipped browser and wrong-tenant redirect cannot certify; valid public receipt links back to requester IAR. No vault-generated PASS without consumer proof |
| FR-NEXTREL-ALPHA-VAULT-002 | Reconcile operator release registry with public skills CompatSet, demo release and hosted provider identities | Drift detected with actionable owner; optional operator audit consumes public artifacts. No private registry access required on subscriber/builder devices |
| FR-NEXTREL-ALPHA-VAULT-003 | Operator service activation/reconciliation and support playbooks for exceptional tenant/store/entitlement failures | Idempotent operator recovery with least-privilege secrets kept private, redacted correlation and audit evidence. Does not replace public self-service activation |
| FR-NEXTREL-ALPHA-VAULT-004 | Provider handoff lifecycle and alpha extraction register | Import preserves IDs and source link; record target IAR, owner, ACCEPT decision, implementation release, test evidence and ABSORBED status back in requester IAR. Never mark absorbed upon copying text alone |

### Review disposition changelog — 2026-09-08

- **Take:** three-repo role separation; registration redirect gap; identity/context gap; unsafe AMA rendering risk; false-green test risk; journal retention bug; release/document drift; guided-preview versus subscriber-alpha distinction.
- **Adapt:** turn observations into owned bugs and separate public/provider FRs, with negative tests and explicit evidence limits. Separate free versus paid alpha, and local-repo independence versus hosted-service dependencies.
- **Reject:** mandatory vault checkout/runtime/operator secrets for standard OC; treating HTTP 200, a marketing page or workbench mount as subscriber onboarding; treating this documentation update as implementation or provider acceptance.
- **Defer for extraction:** private operator/certification improvements only, under FR-NEXTREL-ALPHA-VAULT-001 through 004. Preserve all earlier NextRel IDs and history.
