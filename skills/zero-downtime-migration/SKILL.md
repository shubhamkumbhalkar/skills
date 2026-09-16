---
name: zero-downtime-migration
description: Use when planning or reviewing a zero-downtime migration of a live or Tier-1 service, datastore, or region move. Trigger on "migrate without downtime", "cut over a service", "move/replace a database", "re-platform safely", or "plan a safe rollout with rollback". Produces a phased plan with dual-writes, backfill, shadow verification, incremental cutover, and a rollback at every step.
license: MIT
metadata:
  version: "0.1.0"
  author: Shubham Kumbhalkar
---

# Zero-Downtime Migration

Plan a migration of a live system so that at no point is there downtime, data loss, or an
irreversible step without a tested rollback. This applies to datastore swaps, service
re-platforming, region/account moves, and schema changes on hot tables.

## Core principles

- **Every phase is independently reversible.** Never take a step you cannot roll back.
- **Expand then contract.** Add the new path alongside the old; only remove the old path
  after the new one is proven in production.
- **Verify with real traffic before trusting it.** Shadow/compare before you cut over.
- **Cut over incrementally.** Percentage-based, per-tenant, or per-shard — never big-bang.

## Phased playbook

**Phase 0 — Baseline & safety net**
- Capture current SLOs, throughput, error rate, and p99 latency (your rollback bar).
- Confirm backups/snapshots and a tested restore. Define the rollback trigger and owner.

**Phase 1 — Expand (add the new path, dormant)**
- Stand up the new store/service. Deploy behind a flag, taking no production reads yet.
- Add a dual-write: writes go to old (source of truth) AND new, with the new write
  non-blocking and failures logged, not customer-facing.

**Phase 2 — Backfill**
- Backfill historical data into the new store in batches, throttled to protect the source.
- Make backfill idempotent and resumable. Reconcile counts/checksums old vs new.

**Phase 3 — Shadow & verify**
- Shadow reads: serve from old, also read from new, and compare results (diff rate, latency).
- Drive the diff rate to near-zero. Investigate every mismatch — they are usually real bugs.

**Phase 4 — Incremental cutover**
- Flip reads to the new store for 1% -> 5% -> 25% -> 50% -> 100%, watching the Phase 0 SLOs.
- New store is now source of truth; keep dual-writing to old as the rollback path.
- Roll back instantly (flag flip) if any SLO breaches.

**Phase 5 — Contract (decommission)**
- After a soak period at 100% with healthy metrics, stop writing to the old store.
- Archive/snapshot the old store, then decommission. Remove dead code and flags.

## Review checklist (if reviewing someone's plan)
- Is there a rollback at EVERY phase, or is some step one-way?
- Is the cutover incremental and flag-controlled, or big-bang?
- Is there real-traffic verification (shadow/compare) before cutover?
- Is backfill idempotent, resumable, and reconciled?
- Are dual-writes handled for failure (partial write to one store)?
- Is the rollback trigger defined with an owner and a metric bar?

## Output format

```
## Migration plan: <system>
Rollback trigger: <metric + threshold + owner>

Phase 0 Baseline: ...
Phase 1 Expand: ... (rollback: ...)
Phase 2 Backfill: ... (rollback: ...)
Phase 3 Shadow: ... (rollback: ...)
Phase 4 Cutover: 1/5/25/50/100% ... (rollback: ...)
Phase 5 Contract: ...

### Top risks
- ...
```
