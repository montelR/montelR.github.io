---
title: "Building observable infrastructure with explicit evidence boundaries"
summary: "Project Sentinel combines homelab operations, read-only monitoring and recoverable diagnostics with a development-stage modular AI runtime."
category: "Infrastructure reliability"
status: "Historical evidence · runtime in development"
order: 4
stack: ["Linux","Docker","FastAPI","Python","Monitoring"]
---

## The engineering problem

An administrative interface must distinguish observed health from unavailable or stale readings. Diagnostics should make large output easier to inspect without losing evidence. Model output and authority to act are also different things.

## My role

I direct the project goals, architecture and release decisions, and work with AI coding assistants on implementation, debugging, testing and documentation.

## Architecture and boundaries

Project Sentinel includes a Linux homelab, containerized applications, recovery procedures and a separate recovery and monitoring node. Sentinel API provides read-only monitoring contracts and controlled administrative interfaces. The separate modular runtime explores a primary model, bounded specialists, provider-neutral memory and tool authorization.

The referenced runtime checkpoint is development version 0.1.0. Specialist results do not confer authority. Concrete physical sensor integration and capability-aware execution remain next work. The abstract architecture does not assert that the runtime already controls monitored infrastructure.

## Historical evidence

A November 20, 2026 Sentinel API checkpoint recorded 88/88 full backend tests and 16 focused tests for an opt-in diagnostic utility.

A three-case synthetic benchmark preserved original output while producing compact summaries. Selected noisy failed-test output went from 52,678 original bytes to a 1,824-byte summary (96.5% fewer model-visible bytes). Multi-tool output fell from 16,655 to 1,214 bytes. A tiny successful result grew from 49 to 950 bytes.

The original remained retrievable. These are byte proxies, not measured tokens, cost or general compression performance. The tiny-output counterexample shows that summarization is not automatically useful.

## Reproduce the principle locally

The standalone example in `examples/monitoring/` uses fictional in-memory readings and logs. Fresh healthy and unhealthy readings classify explicitly; stale, absent and future-dated readings return UNKNOWN.

A 5,424-byte fictional log produced a 105-byte summary without changing original bytes. All nine tests passed, including freshness boundaries, missing data and changed evidence. This is a deterministic educational model, not a host monitoring service or production implementation.

## Engineering lesson

Observe before acting, preserve evidence, make uncertainty explicit and separate permission to execute from model output. Document verification and recovery boundaries.

No live infrastructure was queried or changed by this example. Historical tests were not rerun.
