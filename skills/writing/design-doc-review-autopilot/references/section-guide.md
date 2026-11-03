# Design Section Guide

Use this guide to draft or audit the durable source document. Adapt depth to the design, but mark omitted sections as not applicable.

## Contents

- [Required opening](#required-opening)
- [Context and boundaries](#context-and-boundaries)
- [Options and decision](#options-and-decision)
- [Proposed design](#proposed-design)
- [Measurement and delivery](#measurement-and-delivery)
- [Closing sections](#closing-sections)

## Required opening

### Metadata and review request

Include owner, status, scope, intended reviewers, implementation owner, and the exact decision requested. State whether the document covers a final architecture or a directed pilot.

### Executive summary

Answer five questions in a short narrative:

1. What customer or operational problem exists?
2. What exists today?
3. What change is proposed?
4. Why is this option preferred?
5. What must reviewers decide?

## Context and boundaries

### Background and current state

Describe the current request path, systems, data stores, external dependencies, trust boundaries, and known operational process. Include measured scale and failure history when available.

### Problem and evidence

Separate observed problems from assumptions. Link claims to code, configuration, runbooks, incidents, queries, experiments, or customer evidence.

### Goals and non-goals

State outcomes, not implementation choices. For a pilot, include what the pilot must learn and what it intentionally does not prove.

### Requirements and constraints

Cover correctness, compatibility, availability, latency, throughput, security, privacy, operations, staffing, schedule, and reversibility. Mark thresholds that still need approval.

## Options and decision

### Evaluation criteria

Choose criteria before writing the recommendation. Typical criteria include correctness, customer impact, implementation effort, operational load, security, migration, reversibility, dependencies, cost, and future flexibility.

### Credible options

For every viable option include:

- One compact architecture visual
- Normal flow
- State ownership
- Pros and cons
- Failure and rollback implications
- Delivery dependencies
- When the option becomes preferable

Give each option comparable depth. Do not use a detailed diagram for the recommendation and a weak paragraph for alternatives.

### Recommendation

Explain which criteria determine the choice. State the tradeoff being accepted and the evidence that would reverse the decision.

## Proposed design

### Architecture and responsibilities

For each component state owner, responsibility, inputs, outputs, state, source of truth, failure behavior, and what remains outside its boundary.

### Contracts and data model

Define keys, schemas, ordering, idempotency, lifecycle, status transitions, retention, versioning, and compatibility. Distinguish desired state from deployed state.

### End-to-end flow

Cover validation, approval, write ordering, activation, verification, and completion. State when user-visible or downstream success is recorded.

### Failure and recovery

Cover malformed input, partial failure, timeout, duplicate delivery, stale state, concurrency, dependency failure, rollback, data correction, and unknown state. Define the blast radius and stop conditions.

### Security and data handling

Cover data classification, authentication, authorization, least privilege, encryption, local copies, logs, evidence references, retention, deletion, and access verification.

### Operations

Define operator steps, deadlines, metrics, alarms, logs, runbooks, escalation, support owner, backup owner, and recovery target.

## Measurement and delivery

### Measurement

Define the baseline, comparison grain, metric formulas, direction, denominator, missing-data treatment, selection bias, sample unit, confidence method, and authoritative reporting source.

### Success and exit

Separate fixed integrity gates from numeric thresholds. Include continue, expand, add controls, stop, and neutral outcomes. Pre-register thresholds before reviewing results.

### Testing

Test the riskiest claims directly. Include malformed input, idempotent retry, precedence, concurrency, partial failure, final-item removal, reconciliation, rollback, access denial, and hand-computed metrics.

### Rollout and migration

Cover historical replay, shadowing, coexistence, cutover, legacy state, old-writer retirement, rollback, and deprecation.

### Estimate

Use the unit requested by the user. State assumptions and re-estimation gates without turning effort into a delivery commitment.

## Closing sections

### Decision and evidence table

Track each topic as decided, open, evidence required, or implementation task. Add an owner or owner role and closure condition.

### Sources

Link primary evidence. Use placeholders in public templates and never publish private source URLs.
