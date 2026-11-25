---
title: "Reducing repeated retrieval work without sacrificing evidence"
summary: "Indigo Relay grouped bounded source reads into one verified snapshot, reducing repeated acquisition overhead while preserving exact recall."
category: "Tool infrastructure"
status: "Historical benchmark"
order: 3
stack: ["Python","Git","Node.js","Regression testing"]
---

## The engineering problem

Agent-assisted debugging often requires several small reads from the same source revision. Repeating snapshot acquisition for each read adds work. Optimization must preserve access boundaries, the expected revision and the original evidence.

## My role

I direct the project goals, architecture and release decisions, and work with AI coding assistants on implementation, debugging, testing and documentation.

## Design

The retrieval gateway supports bounded source and document operations through provider adapters. Git batch groups up to four child reads in one fresh, revision-verified snapshot. Separate invocations still acquire fresh snapshots. No persistent private Git cache was introduced.

## Historical matched measurements

On November 20, 2026, three live read-only workflows were compared, with three trials per method and the same revision and file/line targets. All 18 trial attempts recalled expected content.

- Targeted source: median elapsed time 1,502.7 ms to 788.0 ms, a 47.6% reduction.
- Multi-file debugging: 2,208.7 ms to 826.3 ms, a 62.6% reduction.
- Architecture documentation: 1,476.8 ms to 755.0 ms, a 48.9% reduction.

Separate reads made two or three acquisition calls; grouping made one. These are historical CLI latency measurements, not packet counts, current performance guarantees or measured tokens or billing. The Phase 3 checkpoint passed 45 Python and 40 Node tests, plus nine installed batch trials.

## Reproduce the principle locally

The separate example in `examples/bounded_retrieval/` creates a disposable fictional Git repository. Two reads used two clones versus one; three reads used three clones versus one. Both paths returned identical original bytes at the expected revision. All seven tests passed, including invalid paths and revisions.

These new operation counts do not reproduce historical network latency or establish production authorization security.

## Engineering lesson

Reduce repeated acquisition rather than discarding evidence. Verify the revision, bound requests and distinguish an operation-count improvement from an end-user performance claim.

The original project was not rerun for this portfolio. No private configuration, endpoint, credential or implementation is included.
