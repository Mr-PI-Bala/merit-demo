# MERIT Demo Ecosystem Plan (SSOT)

**Status:** Plan / controlling IAR until implementation  
**Repo path:** `merit-demo docs/IAR/MERIT_DEMO_ECOSYSTEM_PLAN.md`  
**Updated:** 2026-09-05 (Codex cloud-recovery IAR v2 review merged)  
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
| Page references `merit_workbench@0.4.0` on merit-prod | Configured pin + CDN attempt | Pin equals deployed artifact until inventory | Pin observed; lock after inspect |
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

Public, `Cache-Control: no-store`. Field names/additive merge finalized after live `/api/health` inspect. `0.4.0` is the **observed reference pin** on this consumer until inventory confirms the deployed artifact.

```json
{
  "status": "ok",
  "service": "merit-prod",
  "workbenchVersion": "0.4.0",
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

---

## Test and release gates

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

| FR | Status | Evidence |
|----|--------|----------|
| FR-005-C, FR-006-C, FR-012-C, FR-001-C, FR-003-C, FR-004-C (page pin), FR-011-C | **DONE (Pass 1)** | Playwright: Hosted Ready + mount + Register free; smoke e2e OK; `play/index.html` DualRail states |
| FR-010-C | **PARTIAL** | This IAR + refreshed usage/design/AGENTS/README |
| All other FRs | **PLANNED** | Awaiting Pass 2–4 |

Pass 1 verify: `npm run build && npm run e2e` and `npm run e2e:playwright`. Serve with `npx serve .` → `/play/` → `data-runtime-state="hosted-ready"`.


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
- Pin nuance: treat `0.4.0` as **observed reference** until inventory locks the pin to the deployed artifact.
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

- Live inspect of merit-prod health schema, CORS, and whether `0.4.0` vs registry `0.4.14` should be the locked baseline pin.
- Published here.now URL for this seed (unverified).
- Whether a future **law-approved** optional vendored read-only PAR is ever allowed for richer offline demo (explicitly out of Pass 1).
- Pass 2–4 ownership when writing to skills Hub / merit-prod (may be hand-off).
