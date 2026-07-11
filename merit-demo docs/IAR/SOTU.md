# merit-demo SOTU - 2026-07-11

## Executive status

merit-demo is aligned as the showcase consumer for the upgraded meritutils provider lane. It remains a demo/reference consumer, not a billing authority.

## MERIT utilities usage alignment

Consumer manifest: `cfg/meritutils_consumer.json`.

| Package | Pin | Use |
|---|---:|---|
| `merit_workbench` | `meritutils/merit_workbench@0.4.0` | Shared play/workbench shell |
| `journal` | `meritutils/journal@0.2.2` | Deprecated-compatible legacy journal demo |
| `merit_journal` | `meritutils/merit_journal@0.3.0` | New journal lane |
| `merit_ama` | `meritutils/merit_ama@0.1.0` | AMA question/vote showcase |
| `merit_leaderboard` | `meritutils/merit_leaderboard@0.1.0` | AMA/journal ranking showcase |
| `merit_usage_meter` | `meritutils/merit_usage_meter@0.1.1` | Usage/audit metering |

Default promo is `FREEASINTRO`; affiliate code is `MERITDEMO`. M4FI is intentionally excluded from this closeout.

## E2E TDD plan

| Persona | Path | Assertion |
|---|---|---|
| Community member | `/play/` | workbench loads from PAR CDN and routes into demo surfaces |
| AMA participant | AMA showcase | asks/votes remain usage-meterable with `FREEASINTRO` |
| Journal user | journal showcase | `journal@0.2.2` remains legacy-compatible while `merit_journal@0.3.0` is the forward path |
| Operator | usage manifest | missing promo resolves to `FREEASINTRO`; affiliate remains `MERITDEMO` |

## Closeout note

Provider validation completed upstream: meritsubs default promo tests pass and meritstore FREEASINTRO zero-dollar checkout Playwright passes.
