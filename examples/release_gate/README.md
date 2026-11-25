# Fictional paired evaluation and release gate

A standalone standard-library Python exercise about evidence-based development decisions. The fixtures represent invented document-review outcomes, not exported Sentinel Work cases. No browser, network, model, credentials or production code is involved.

The evaluator counts matching outcomes across both arms, checks that unauthorized effects are absent and necessary notices are unchanged, and computes the reduction using only predeclared eligible cases. A development PASS requires all outcomes to match, at least 25% eligible reduction, and positive net improvement across two distinct, independently defined mechanisms. A safety violation yields FAIL; insufficient usefulness evidence yields HOLD. A missing eligible denominator also yields HOLD. The evaluator assumes trusted, predeclared mechanism and eligibility labels; it does not discover or prove independence.

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s examples/release_gate -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=examples/release_gate python3 -c 'from fixtures import HOLD_CASES, SECOND_MECHANISM; from gate import evaluate; print(evaluate(HOLD_CASES)); print(evaluate(HOLD_CASES + (SECOND_MECHANISM,)))'
```

| Fictional fixture | Correct outcomes | Eligible notices | Improving mechanisms | Verdict |
| --- | --- | --- | --- | --- |
| Seven pairs, five variants of one mechanism | 14/14 | 5 to 0 | 1 | HOLD |
| Eight pairs, including an invented second mechanism | 16/16 | 6 to 0 | 2 | PASS (development gate only) |

The 11 tests cover both verdicts, incorrect classifications, unauthorized effects, necessary-review suppression, the threshold boundary, below-threshold usefulness, a missing denominator, duplicate IDs, negative counts and empty samples.

Measured on November 24, 2026 ET: all 11 tests passed; both fixture verdicts were printed. The fixture's added second mechanism is hypothetical and does not establish a second useful Sentinel Work mechanism or change its historical HOLD. These are deterministic educational policy tests, not new measurements of model performance, user interruptions or production readiness.
