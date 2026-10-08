# User brief and research — 8 October 2026

State: RESEARCHED → BUILDING.

User: Data engineers verifying pseudonymized CSV exports before downstream joins.

Painful task: Export transformations can silently break identifier linkage or collapse distinct identifiers. Independent checking is useful when the transformation engine is outside the team's control.

Smallest useful capability: Audit row-aligned source/masked export pairs for unchanged/erased identifiers, per-domain collisions, inconsistent tokens and changed non-ID anchor cells; reports omit cell values.

Demand is inferred from the documented workflows and review risks. No verified request for this product, adoption, performance advantage or exhaustive feature gap is claimed. Search and repository/README/code/issue reads occurred on 8 October 2026; current exact stars and last-push timestamps below are observations, not quality scores.

Queries: `csv pseudonymization sort:stars; csv anonymization in:description sort:stars`. Live GitHub search used `sort:stars`. Broad queries return unrelated repository/readme matches; irrelevant results were excluded. Coverage is limited, not an exhaustive global ranking. The highest-star relevant comparable among those examined is [ikuV/deident-wasm](https://github.com/ikuV/deident-wasm) at 166 stars.

| Comparable | Stars | Last push (UTC) | License | Workflow, setup, capabilities and tradeoffs |
|---|---:|---|---|---|
| [ikuV/deident-wasm](https://github.com/ikuV/deident-wasm) | 166 | 2026-08-23T15:09:41Z | Apache-2.0 | Rust/WASM privacy transformations, explicit policy domains, chained datasets, linkage checks, risk reports and documented limitations. It already handles linked exports: no claim that our audit fills an absent feature. Our standalone verifier checks externally produced row-aligned pairs. |
| [fabriziosalmi/csv-anonymizer](https://github.com/fabriziosalmi/csv-anonymizer) | 10 | 2026-09-06T11:22:10Z | AGPL-3.0 | Browser CSV transformations using heuristic column typing and fuzzing/redaction. README explicitly requests checking output before sharing. Our read-only verifier checks declared identifier mapping invariants, not privacy. |
| [fgmacedo/datanonymizer](https://github.com/fgmacedo/datanonymizer) | 9 | 2026-09-22T19:07:25Z | MIT | Python CSV conversion with fake generators and documented command examples. Focuses on producing modified data; our verifier accepts source/masked pairs without choosing a transformation engine. |

Reliability/support observations are limited to public docs, latest source and open issue samples; alternatives were not installed or benchmarked in this run. Examples prove our behavior only. No comparative speed, memory, accuracy or time-to-result measurement was made. Licenses are metadata observations; no competitor implementation/prose was reused.

Acceptance: documented clean install; accepted example; meaningful rejected/input-error examples; deterministic JSON reports; core invariants covered by the unit tests; all remote matrix checks must pass on the intended default head before LIVE. The exact scope/non-goals are in README.md.

Discovery path: relevant GitHub topics and a clear README/linked portfolio index. No messages or third-party issue advertising planned, and no organic growth promise.

Portfolio distinction: compared against all 143 existing repository names/descriptions and relevant CSV/HTTP/parser tools. This is not a fork or a variant of an existing launch. The five candidates address spatial delivery, cache deployment intent, CSP inheritance changes, crawler route expectations and cross-export identifier mapping respectively. masklink-audit does not reconcile numeric CSV differences like table-reconcile, transform data or copy a redaction engine. They are separate user tasks, not subdivisions of one product.

## Commit-linked observations

- [ikuV/deident-wasm source snapshot](https://github.com/ikuV/deident-wasm/tree/f95ab50b0a893dd9de273ebfc4e419c2f2e1a223) — open issue sample: none returned.
- [fabriziosalmi/csv-anonymizer source snapshot](https://github.com/fabriziosalmi/csv-anonymizer/tree/0347d41e1cd4fe4b4312344cbdd0a39bcd226235) — open issue sample: none returned.
- [fgmacedo/datanonymizer source snapshot](https://github.com/fgmacedo/datanonymizer/tree/ee68a62efb0bc007c5b288a93a5f069be012d200) — open issue sample: none returned.

Standards consulted: [GeoJSON RFC 7946](https://www.rfc-editor.org/rfc/rfc7946.html), [HTTP caching RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html), [Robots RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html), [CSP3](https://www.w3.org/TR/CSP3/). Only the relevant standard informs each bounded tool; conformance is not claimed.
