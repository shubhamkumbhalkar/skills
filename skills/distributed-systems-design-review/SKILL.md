---
name: distributed-systems-design-review
description: Use when reviewing a distributed-systems design, RFC, architecture, or PR for reliability and correctness at scale. Trigger on requests to review a system design, critique an architecture, or check whether a service is production-ready under real load. Surfaces idempotency, retry, backpressure, consistency, failure-mode, and observability gaps before they cause incidents.
license: MIT
metadata:
  version: "0.1.0"
  author: Shubham Kumbhalkar
---

# Distributed Systems Design Review

You are reviewing a distributed system for the failure modes that cause real production
incidents. Be specific and blunt: name the exact scenario, the blast radius, and the fix.
Do not rubber-stamp. If the design is sound, say so and explain why.

## How to run the review

1. Restate the system in one paragraph: the request path, the data stores, the external
   dependencies, and the trust/consistency boundaries. If any are unclear, ask before reviewing.
2. Walk each dimension below. For every gap, output: **Risk** (the concrete failure scenario),
   **Impact** (blast radius / who is affected), and **Fix** (a specific, minimal change).
3. End with a short verdict: Ship / Ship with changes / Needs rework, and the top 3 must-fix items.

## Dimensions

**Idempotency & exactly-once illusions**
- Can every write be safely retried? Is there an idempotency key on mutating endpoints and
  queue consumers? What happens on duplicate delivery (queues are at-least-once)?
- Are non-idempotent side effects (payments, emails, external calls) deduped or made idempotent?

**Retries, timeouts & backpressure**
- Does every network call have a timeout and a bounded retry with jittered exponential backoff?
- Are retries capped to avoid retry storms and cascading failure? Is there a circuit breaker?
- Is there backpressure (bounded queues, load shedding, rate limits) so a slow dependency
  does not exhaust threads/connections upstream?

**Consistency & data model**
- What consistency does each read need (strong vs eventual)? Are cross-store writes atomic,
  or is there a saga/outbox with compensations? Is dual-write drift possible?
- Are there read-modify-write races? Optimistic concurrency / conditional writes where needed?

**Failure modes & blast radius**
- What happens when each dependency is down, slow, or returns garbage? Is there a fallback or
  graceful degradation? Is failure isolated (bulkheads) or does it take down the whole service?
- Single points of failure? What is the behavior across an AZ/region failure?

**Scaling & hotspots**
- Where are the hot keys / hot partitions? Does the partition key spread load evenly?
- What breaks first at 10x traffic — a connection pool, a DB, a single-threaded stage?

**Observability & operability**
- Are the golden signals (latency, traffic, errors, saturation) emitted per dependency?
- Can you detect the failure modes above from metrics/alarms before customers do?
- Is there a runbook, a rollback path, and a way to shed load or disable a feature fast?

**Security & data**
- AuthN/AuthZ on every entry point? PII handling and least-privilege access?
- Input validation and safe handling of untrusted upstream data?

## Output format

```
## Verdict: <Ship | Ship with changes | Needs rework>

### Must-fix (top 3)
1. ...

### Findings by dimension
- [Idempotency] Risk / Impact / Fix
- [Retries] Risk / Impact / Fix
...

### What's already solid
- ...
```
