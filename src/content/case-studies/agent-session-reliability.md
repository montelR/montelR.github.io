---
title: "When successful interaction is not proof of authorization"
summary: "A Sentinel Work investigation separated positive workflow evidence from permission to continue, reproduced a boundary failure and verified a targeted correction."
category: "Failure investigation"
status: "Historical synthetic evidence"
order: 1
stack: ["Python","Chromium","Regression testing"]
---

## The engineering problem

Sentinel Work explores reliable agent-assisted browser workflows. When an automated workflow pauses for human review, a successful interaction can provide evidence that a prerequisite was met. That evidence does not, by itself, establish who may continue the workflow.

The expected behavior required both valid evidence and appropriate authority over the original session. A November 2026 synthetic review found a case in which continuation was accepted without sufficient owner authority. The failure concerned the decision boundary, not whether the interaction itself succeeded.

## My role

I direct the project goals, architecture and release decisions, and work with AI coding assistants on implementation, debugging, testing and documentation. The following results describe documented project checkpoints, not a claim of sole authorship or an external human security audit.

## Investigation and correction

The project reproduced the original negative result against the uncorrected source before changing the implementation. A focused regression encoded the expected denial. The corrected design kept positive evidence as a mandatory prerequisite and separately checked continuation authority and original-session integrity.

The regression failed before the change and passed afterward. A separate source-pinned re-review froze its expected outcomes before execution, checked which executable revision actually ran and examined observable behavior rather than trusting a successful command response alone.

The engineering lesson is to separate what happened, whether it satisfies a prerequisite, and whether the requested action is authorized. An uncertain or invalid condition should not silently grant permission.

## Verification and release decision

- **November 20, 2026 repair:** 194/194 selected Python regressions; 53/53 real Chromium tests.
- **November 21, 2026 separate re-review:** 19/19 new offline adversarial scenarios; zero final submission effects.
- **November 21 supporting suites:** 197/197 selected Python tests; 10/10 evidence-integrity checks; 12/12 native Mac Debug XCTest.
- **November 21 iOS verification:** Generic physical-device-target compilation passed; no physical iPhone acceptance.

The suites may overlap and must not be added together. The re-review passed its tested synthetic boundaries, not production release clearance. It did not establish distinct human cryptographic identity or clear a separately documented legacy interface.

## Reproduce the principle: fictional review handoff

A new, standalone Python example models an unrelated fictional document review. It demonstrates the decision-rule distinction without reproducing the private browser protocol or using any live system.

The baseline requires positive evidence, the matching document and revision, and an open review. The corrected rule also requires the actor to be the designated reviewer.

**Baseline: 6/8 passed. Corrected: 8/8 passed.**

The two failing baseline assertions involved a different actor and a missing actor. The corrected policy passed those same tests without changing the expectations.

The example lives in the portfolio repository under `examples/session_handoff/`. Its README includes the two commands and expected outcomes. It uses only the Python standard library, operates on fictional in-memory data, and performs no external action. It is an educational model rather than the original implementation, authentication system, or production security test.

## What this demonstrates

The investigation illustrates testable requirements, a reproducible negative result, a narrow correction, independently specified expectations and honest release boundaries. A passing test suite is evidence for the conditions it covers, not automatic permission to deploy.

The historical records were not rerun for this portfolio. The eight-test fictional demonstration is separately executed portfolio evidence.
