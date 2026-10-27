# Critic Panels

## Contents

- [Finding classification](#finding-classification)
- [Deep engineering panel](#deep-engineering-panel)
- [Meeting panel](#meeting-panel)
- [Neutral reviewer prompt](#neutral-reviewer-prompt)
- [Synthesis contract](#synthesis-contract)
- [Revision and stopping policy](#revision-and-stopping-policy)

## Finding classification

Every reviewer MUST classify each finding:

| Class | Meaning |
| --- | --- |
| Document blocker | Contradiction, impossible mechanism, unsupported recommendation, missing credible option, or insufficient information for the requested decision |
| Evidence gate | Design is understandable, but implementation or launch needs proof |
| Team decision | Product, policy, risk, threshold, ownership, or preference choice |
| Optional improvement | Helpful but unnecessary for the decision |

Reviewers MUST NOT convert evidence gates into document blockers because proof is still pending. Reviewers MUST NOT downgrade contradictions to evidence gates merely to produce a passing verdict.

## Deep engineering panel

Run six independent reviewers in parallel:

| Reviewer | Lens |
| --- | --- |
| Service correctness | Contracts, state, consistency, ordering, idempotency, concurrency, compatibility |
| Operations and recovery | Activation, partial failure, retry, rollback, runbook, support, recovery time |
| Security and data | Authentication, authorization, least privilege, classification, local copies, logs, retention |
| Measurement and data science | Baseline, metric math, missing data, bias, sample unit, confidence, exit rules |
| Product and scope | Customer problem, eligibility, goals, exclusions, experience, expansion choices |
| Document and decision quality | Background, option fairness, evidence, readability, ownership, decision clarity |

Each reviewer SHOULD return:

1. Verdict for its lens
2. Strengths
3. Findings with class and evidence
4. Likely reviewer questions
5. Minimal edits

Use a seventh independent reviewer to synthesize, deduplicate, and resolve disagreements by evidence quality.

## Meeting panel

Run these ten personas once after the companion document is stable:

1. Technical program manager
2. Engineering manager
3. Product manager
4. Senior software engineer
5. Primary service owner
6. Downstream service owner
7. Operations user
8. Security reviewer
9. Data scientist
10. Analytics or dashboard owner

Each persona asks three or four questions they would realistically raise in the scheduled meeting. Require:

- Question
- Answerability: short document, full design or evidence, open decision, or missing
- Best current answer in one to three sentences
- Meeting action: answer, decide, assign, or park

The synthesis MUST produce the 15 most likely deduplicated questions, not merely say that a synthesis was completed.

## Neutral reviewer prompt

Use this structure and replace bracketed values:

```text
You are the [reviewer role] reviewing [artifact] through the lens of [neutral lens definition].
Read the current artifact and cited evidence. Ask realistic questions and identify strengths or gaps within this lens only.
Classify every finding as document blocker, evidence gate, team decision, or optional improvement.
Give a concise evidence-backed answer when available. Do not invent missing facts. Do not edit or comment on the artifact.
```

Do not tell the reviewer which defects are expected. Prior findings MAY be supplied only when the task is to verify whether a known issue was fixed.

## Synthesis contract

The synthesis reviewer MUST return:

1. Binary team-review readiness
2. Binary implementation readiness
3. Deduplicated blockers ordered by impact
4. Evidence gates with owners or owner roles
5. Team decisions the meeting must close
6. Optional improvements
7. A question-and-answer matrix
8. A bounded next-edit list

The synthesizer MUST resolve disagreements using direct evidence, then primary-source evidence, then majority agreement. It MUST preserve minority findings when the evidence remains unresolved.

## Revision and stopping policy

The orchestrator MAY apply automatic edits only when evidence supports one clear correction. It MUST ask the user before selecting a product, policy, risk, threshold, or ownership decision.

Run at most:

- Two deep engineering rounds
- One meeting panel
- One final deterministic consistency scan

After the limit, freeze the document when remaining items are evidence gates, team decisions, or optional improvements. Additional review requires an explicit user request.
