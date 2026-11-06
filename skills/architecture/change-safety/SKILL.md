---
name: change-safety
description: "Research the real apply mechanism, map failure modes and recovery, and self-critique for a safer option BEFORE making any change. Use when raising or merging a CR, running a manual command (AWS, CLI, git, infra), editing config or IaC, deploying, promoting a pipeline artifact, deleting or disabling a resource, or doing any step that is hard to reverse or touches a shared or production system. Use when a green build or passing synth is being treated as proof that a change is safe to apply. Triggers: raise a CR, merge this, deploy, promote, delete stack, run this in prod, disable, tear down, is this safe."
tags: [architecture, change-management, deployment, pre-mortem, self-critique, operations]
---

# Change Safety

## Overview
Before any change, verify that the system can safely **apply** it, not just that it builds. Most
production incidents come from skipping two steps: researching how the target system actually
applies the change, and pre-morteming the failure before it happens. This skill forces both.

## Usage
Use this skill before you:
- Raise, approve, or merge a code review (CR).
- Run a manual command that mutates state — AWS CLI/console, `git`, infra, DB, config.
- Deploy, promote a pipeline artifact, or change a pipeline/deployment definition.
- Delete, terminate, disable, or scale a resource.
- Edit IaC (CDK/CloudFormation/Terraform), a build config, or a pipeline definition.
- Tell the user "this is safe" or "this will work."

Skip it only for genuinely trivial, local, reversible work (reading, local scratch files, a
draft you will not send). When unsure whether it is trivial, run the skill.

## Core Concepts

**Build-safe is not apply-safe.** A passing build, `cdk synth`, or green CI proves the artifact
is *well-formed*. It does not prove the live system can *apply* it without failing, wedging, or
cascading. Name the real signal before trusting a cheap proxy for it.

**Every change has an apply mechanism.** Something takes your artifact and makes it live — a
self-mutating pipeline, a deploy engine, CloudFormation, a merge queue, a DB migration runner.
The mechanism has ordering, preconditions, and its own failure modes. If you cannot describe the
mechanism in one or two sentences, you have not researched enough to change it.

**Reversibility sets the bar.** The harder a change is to undo, the more research and the more
explicit the pre-mortem. Irreversible or production-facing changes get the full workflow and a
confirmation gate with the user.

## Workflow: Research, Critique, Gate

You MUST run all three phases in order. You MUST NOT act until the gate passes.

### 1. Research the mechanism
Answer these before you touch anything. Use evidence (docs, code, live reads), not memory.
- **How is this applied?** Name the engine and the exact sequence of steps it runs.
- **What runs first?** Ordering bugs hide here (e.g. self-mutation before deployment groups,
  schema migration before code, export deletion before its importer).
- **What does it depend on, and what depends on it?** Map upstream inputs and downstream
  consumers. A change that looks local can be imported, referenced, or gated elsewhere.
- **What is the real success signal?** Distinguish "builds" from "deploys" from "applies" from
  "the downstream thing still works." Verify the one that matters, not the cheapest one.

### 2. Critique — pre-mortem before it happens
Assume the change has gone live. Then ask:
- **What are the failure modes?** List at least the top two concrete ways this breaks on apply.
  For each: what is the blast radius, and is it reversible?
- **What am I assuming?** List the assumptions this depends on. Mark each as verified or
  unverified. An unverified assumption on an irreversible change is a stop.
- **What is the recovery?** If it fails, what is the exact undo? Does the undo need a revert, a
  new approval, a break-glass, or someone else? If recovery is unknown, you are not ready.
- **Is there a simpler or safer path?** Challenge your own plan. Often a manual, scoped,
  reversible action beats a clever automated one — or the reverse. State why the chosen path
  wins over the obvious alternative.

### 3. Gate — state risk, then act
- For anything hard to reverse or production-facing: tell the user, in plain words, the top
  failure mode, the blast radius, and the recovery, **before** the irreversible step. Get
  explicit confirmation.
- Honor standing safety rules (production-safety, builder-security). If the change weakens a
  protection or exposes a surface, follow those skills as policy.
- Act, then verify the **real** success signal from phase 1 — not the proxy.

## Quick Reference

Pre-change checklist (all must be answerable):

| # | Question | Stop if |
|---|----------|---------|
| 1 | What engine applies this, and in what order? | You can't describe it |
| 2 | What depends on it / what does it depend on? | Unknown downstream consumers |
| 3 | What is the real success signal (apply, not build)? | You'd only check the build |
| 4 | Top 2 failure modes + blast radius? | Any is production and unmapped |
| 5 | Is it reversible? Exact recovery path? | Recovery unknown or needs others |
| 6 | Unverified assumptions? | Any, on an irreversible change |
| 7 | Simpler/safer alternative considered? | You skipped the comparison |
| 8 | User told the risk before the irreversible step? | Not yet, and it's prod |
| 9 | Command's preconditions confirmed against a fresh read (not copied from the last target)? | You pattern-matched it |

## Common Traps

- **Green-build complacency.** "`synth`/CI passed, so it's safe to merge." It proves form, not
  apply. See phase 1, success signal.
- **Last-item removal.** Removing the final stack, route, consumer, or migration often leaves an
  empty or degraded state the apply engine can't handle. Check what "zero of these" does.
- **Self-mutating systems.** A pipeline or controller that reconfigures itself applies the
  *latest* definition first and can wedge the whole flow, including gates downstream of the
  failure. Research the self-mutation step explicitly.
- **Proxy verification.** Checking the thing that's easy to check instead of the thing that
  matters. Verify the downstream effect, not the local artifact.
- **Deferred recovery thinking.** Figuring out the undo only after it breaks. Know the recovery
  before you commit.
- **Automation bias.** Forcing a change "through the system" when a scoped manual action is
  simpler and more reversible — or automating when manual would drift. Pick on evidence.
- **Unchecked command preconditions.** Handing over or running a command whose precondition
  does not hold in the current state — a flag or mode valid only in a specific status, a
  resource assumed to exist or to be in a given state. Confirm the precondition against a fresh
  read before issuing the command.
- **Pattern-matching across targets.** Copying the exact command that worked on the last
  account, stack, region, or iteration onto the next without re-verifying — regions, statuses,
  names, and preconditions differ per target. Check each target on its own.

## Worked Example: the self-mutating pipeline wedge

A CR removed the last CDK stack from a live self-mutating pipeline. Build and `synth` passed, so
it was merged. On apply it wedged the whole pipeline and blocked the production path.

- **Phase 1 would have caught it:** the pipeline self-mutates to the latest revision *before*
  deployment groups run. "Zero stacks" makes the self-mutation's stack update fail. The real
  success signal was "the pipeline self-mutation and deploy succeed," not "synth passed."
- **Phase 2 would have caught it:** failure mode = self-mutation fails and re-writes/cancels the
  downstream prod approval workflow (blast radius: the whole pipeline, including prod).
  Reversible only by reverting the CR or deleting the pipeline. A simpler path existed —
  termination protection was already off and `DeleteStack` was never denied, so scoped **manual
  deletion** was lower-risk than forcing it through the pipeline.
- **Phase 3 would have surfaced it:** telling the user "this can wedge the pipeline and the only
  recovery is a revert or manual teardown" before merging would have changed the decision.

Lesson: verify apply, not build; pre-mortem the mechanism; prefer the reversible path.
