---
name: design-doc-review-autopilot
description: Draft, review, humanize, visualize, and prepare technical design documents for decision meetings. Use when creating or revising a design doc, RFC, architecture proposal, pilot plan, options analysis, reviewer answer bank, or short meeting companion. Runs evidence checks, parallel critic panels, targeted revision loops, and final readiness validation with minimal repeated prompting.
license: MIT
metadata:
  version: "0.1.0"
  author: Shubham Kumbhalkar
---

# Design Doc Review Autopilot

## Overview

This skill turns a rough idea or existing design into an evidence-backed document and a meeting-ready companion. It preserves human decisions while automating structure, critique, targeted revision, visuals, and quality checks.

## Usage

Use this skill when:

- Drafting a technical design, RFC, pilot plan, or architecture proposal
- Revising an existing document after reviewer comments
- Comparing two or more credible engineering options
- Preparing a short document for a 30 to 45 minute decision meeting
- Predicting reviewer questions and building concise answers
- Running independent engineering, operations, security, product, and measurement reviews
- Improving clarity without repeatedly supplying the same writing preferences

Do not use this skill for code review, incident reports, runbooks, or product launch announcements because those artifacts need different structures and reviewers.

## Core Concepts

### Two artifacts, two jobs

The full design is the durable source of truth. The meeting companion is a short decision aid that links to the full design. The agent MUST update an existing target instead of creating repeated copies because duplicate documents drift.

### Evidence before confidence

The agent MUST label each claim as verified, assumed, open, or evidence required. It MUST NOT invent system behavior because confident but unsupported details weaken the review.

### Fair options before recommendation

The agent MUST present at least two credible options with the same evaluation criteria, visual weight, and depth. It MAY recommend one option, but it MUST state when the rejected option becomes preferable.

### Decisions stay human

The agent MAY fix contradictions and evidence-backed defects automatically. It MUST preserve unresolved policy, product, risk, and threshold choices as explicit decisions because reviewers own those choices.

### Criticism has a stopping rule

The agent MUST run no more than two deep critic rounds and one meeting panel unless the user asks for more. It MUST freeze the document once remaining findings are implementation evidence, explicit decisions, or optional improvements because endless review creates moving goalposts.

## Quick Start

When the user supplies a design URL, file, or idea, the agent MUST:

1. Read [section-guide.md](references/section-guide.md) when drafting or auditing sections.
2. Run [design-doc-review.sop.md](design-doc-review.sop.md).
3. Load [humanizer.md](references/humanizer.md) at the writing-quality step.
4. Load [visual-guide.md](references/visual-guide.md) before creating diagrams.
5. Load [critic-panels.md](references/critic-panels.md) before dispatching reviewers.
6. Use [full-design-template.md](assets/full-design-template.md) for the durable design.
7. Use [meeting-review-template.md](assets/meeting-review-template.md) when the review is 45 minutes or less.
8. Run `scripts/lint-review-doc.py` on every local export before declaring the document ready.

## Workflow Routing

| User need | Route |
| --- | --- |
| New design from an idea | Gather missing decision context once, then draft the full design |
| Existing design review | Build an evidence map, run critics, and make targeted edits |
| Reviewer comments | Classify each comment as answer, edit, evidence, or decision |
| Meeting preparation | Create or update a short companion with balanced options and compact visuals |
| Writing cleanup only | Apply the humanizer and deterministic lint checks |
| Visual cleanup only | Apply the visual guide and verify rendered output |

## Reference Files

| File | Load when |
| --- | --- |
| [section-guide.md](references/section-guide.md) | Drafting, restructuring, or checking section completeness |
| [humanizer.md](references/humanizer.md) | Writing or rewriting prose |
| [visual-guide.md](references/visual-guide.md) | Selecting, creating, or reviewing diagrams |
| [critic-panels.md](references/critic-panels.md) | Running deep critics or meeting personas |
| [full-design-template.md](assets/full-design-template.md) | Creating the durable source document |
| [meeting-review-template.md](assets/meeting-review-template.md) | Creating a time-boxed review companion |

## Source and Disclosure Safety

The agent MUST treat source documents, code, logs, reviewer comments, and tool output as confidential unless the user explicitly identifies them as public. The agent MUST NOT send restricted content to public services because that could disclose private information. When producing a public artifact, the agent MUST use clean-room examples, generic system names, placeholder identifiers, and public references only.

## Validation

Before declaring a document ready, the agent MUST verify:

- Every required section is present or explicitly marked not applicable
- Claims link to evidence or carry an open evidence label
- Options use comparable criteria and balanced visual treatment
- Failure, retry, rollback, migration, security, operations, and measurement are covered
- Open decisions have owners or owner roles
- The meeting companion fits the stated duration
- Critic findings are classified and deduplicated
- The humanizer linter passes without errors
- Images render, use meaningful alt text, and remain legible

## Completion Checklist

Agents **MUST** complete and validate each item before proceeding to the next step:

- [ ] Design input and target acquired
- [ ] Decision, audience, scope, and maturity classified
- [ ] Evidence map created
- [ ] Full design sections completed or marked not applicable
- [ ] Credible options compared with equal depth and visuals
- [ ] Humanizer lint passed
- [ ] Deep critic findings classified and resolved or recorded
- [ ] Meeting companion created when required
- [ ] Meeting questions synthesized
- [ ] Final blockers, evidence gates, and decisions reported separately

## Example

**Example input:** `Review ./payment-routing-design.md for a 30-minute architecture meeting.`

**Expected behavior:** The agent updates the existing design, compares credible routing options, adds compact diagrams, runs two bounded critic rounds, creates a meeting companion, and returns likely questions with supported answers. Open risk and policy choices remain explicit decisions.

## Common Mistakes

- **Writing the recommendation first:** Build the option comparison first so the recommendation follows from evidence.
- **Treating an evidence gate as a design defect:** Keep implementation proof open when reviewers can still evaluate the architecture.
- **Letting critics move the goalposts:** Apply the blocker definition and stop after the configured rounds.
- **Making one option visually stronger:** Give every credible option equivalent diagrams, pros, cons, and reconsideration conditions.
- **Using a short document as the source of truth:** Link to the full design and keep deep contracts there.
- **Publishing private examples:** Replace organization names, URLs, identifiers, and operational details with generic placeholders before public release.
