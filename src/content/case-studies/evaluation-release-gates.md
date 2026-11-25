---
title: "Why passing tests did not justify releasing a feature"
summary: "All 28 matched synthetic outcomes were correct, yet the feature remained on hold because its measured benefit did not generalize across two independent mechanisms."
category: "Evaluation methodology"
status: "Historical evaluation · HOLD"
order: 2
stack: ["Python","Synthetic evaluation","Release criteria"]
---

## The decision

A proposed Sentinel Work change aimed to reduce unnecessary owner-review notifications while preserving legitimate requests for review. The engineering question was not simply whether the change worked in a few examples. It was whether the evidence justified promoting it.

## My role

I direct the project goals, architecture and release decisions, and work with AI coding assistants on implementation, debugging, testing and documentation. The evaluation below describes a documented project checkpoint; it is not an independent human audit or a new production trial.

## Controlled comparison

The November 20, 2026 evaluation froze its protocol, expected outcomes and implementation revision before running 14 paired development cases. Both arms used the same pinned implementation and isolated fictional fixtures; the candidate enabled only the bounded recheck being evaluated. The experiment used disposable state, network isolation and intercepted final actions.

Two separate criteria were established in advance:

- **Safety and correctness:** expected case classifications and notification counts must match; no unauthorized final effects or duplicate deliveries.
- **Usefulness and generalization:** at least 25% reduction in eligible avoidable grouped notices, demonstrated across at least two independently eligible causal patterns.

## Measured historical results

- Baseline: 14/14 expected case outcomes; 11 grouped owner-review intents.
- Candidate: 14/14 expected case outcomes; 6 grouped owner-review intents.
- Across both arms: 28/28 matched expectations, zero guarded final actions, zero external egress attempts and zero duplicate deliveries.
- Within the eligible subset: grouped intents declined from five to zero, a 100% reduction across five variants of **one** causal mechanism.

The overall count of 11 to 6 includes necessary or ineligible requests. Grouped intents are a synthetic notification proxy, not measured interruptions or human time savings. No human-active minutes were recorded.

## Why the verdict was HOLD

The safety gate passed within the tested synthetic boundaries. The numeric usefulness threshold was met, but the independence requirement was not. Five variants of one mechanism do not provide evidence of two independent mechanisms.

A subsequent read-only feasibility review did not identify a credible second independently eligible mechanism under the unchanged implementation. It did not alter the original results, broaden the feature or relax the release criteria. The historical decision remained HOLD / DO NOT PROMOTE. The evaluated feature was default-off and was not deployed by this evaluation.

## Reproduce the decision: fictional release gate

A new standalone Python example in the portfolio repository, `examples/release_gate/`, evaluates invented document-review outcomes against a simplified, predeclared gate. It is separate from the original Sentinel Work evaluation.

- Seven fictional pairs: 14/14 expected outcomes, eligible notices reduced from five to zero, one improving mechanism. Verdict: **HOLD**.
- An additional hypothetical independent mechanism: 16/16 expected outcomes, six to zero eligible notices, two improving mechanisms. Verdict: **PASS** for this fictional development gate only.

All 11 tests passed, including safety violations, required-review suppression, the usefulness threshold boundary, a missing denominator and malformed input. The README gives reproducible commands using only the Python standard library.

The example tests decision logic, not how a model or browser behaves. Its hypothetical second mechanism is not evidence of a second mechanism in Sentinel Work. Mechanism independence and eligibility must be established separately before evaluation.

## Engineering lesson

A good evaluation can produce a useful negative release decision. Freeze the criteria, preserve the denominator, distinguish repeated variants from independent causal coverage, and keep safety and usefulness decisions separate. A high pass count cannot substitute for evidence that an improvement generalizes.

Historical project tests were not rerun for this article. No held-out or live employer cases were used.
