---
name: evidence-traced-threat-model
description: Point an AI coding agent at a repository and get a threat model where every finding cites a real file and line. Picks an architecture profile and a threat modeling method, then forces the agent to prove each claim from source, config, and infrastructure code before it ranks risk or proposes fixes.
tags: [security, threat-modeling, ai-agents, code-review, prompt-engineering, appsec]
---

# Evidence-Traced Threat Model

## Overview

Most agent-generated threat models read like a security textbook. They list SQL injection for a service with no database and skip the IAM role that lets any Lambda read every bucket. The fix is cheap: make the agent cite source before it claims risk.

This skill wraps that discipline into one reusable run. You give the agent a repo, a system type, and a method. It walks the code, builds a component and trust-boundary inventory from real files, enumerates threats against that inventory, and attaches a `path:line` citation to every single finding. Anything it cannot cite gets stamped `ASSUMPTION` and listed separately, so a human reviewer knows exactly where the model is guessing.

The approach follows the pattern popularized by [grim-prompter](https://github.com/jmanico/grim-prompter) (MIT, Jim Manico): a matrix of architecture profiles crossed with threat modeling methods, driven from inside your coding agent instead of a whiteboard. Works in Claude Code, Codex, Cursor, Kiro, or any agent with file read and grep.

Output is a markdown document plus a ranked fix list you can turn into tickets the same day.

## Usage

### When to use

- You inherited a service and need to know what can hurt you in the next 90 days.
- A design is close to launch and someone asks for a threat model artifact.
- You are adding a network listener, an auth path, a file upload, or a new data store.
- You are shipping agent features: tool calling, MCP servers, RAG pipelines, autonomous workflows. Prompt injection and tool-abuse paths need their own pass.
- A pentest or audit is scheduled and you want to find the obvious things first.
- You want a security review meeting where the discussion starts from code, not from opinion.

### When not to use

- No repository access. A design-only system needs a human workshop, not this.
- You need exploit code or an active test against running infrastructure. Out of scope on purpose.
- Compliance paperwork mapping to a control catalog. Different artifact, different prompt.
- A 50-line script with no network, no secrets, and no untrusted input. Read it yourself.
- You plan to ship the output unreviewed. Treat every finding as a hypothesis until a human confirms it.

### Pick an architecture profile

Choose the one closest match, then name the gaps in the scope block.

| Profile | Focus areas |
|---|---|
| Public REST API | AuthN/AuthZ per route, rate limits, input validation, IDOR |
| Internal microservice | Service-to-service identity, mTLS, replay, over-broad trust |
| Serverless event pipeline | IAM blast radius, event source trust, poison messages, idempotency |
| Single-page app plus API | Token storage, CORS, CSRF, XSS sinks, redirect handling |
| Mobile client backend | Device attestation, cert pinning, offline cache, client-side secrets |
| Multi-tenant SaaS | Tenant isolation in queries, keys, caches, logs, and background jobs |
| Data/ETL platform | Lineage, PII flow, column-level access, secrets in job configs |
| CI/CD and build system | Pipeline injection, artifact signing, token scope, dependency confusion |
| LLM agent with tools | Prompt injection, tool allowlists, sandboxing, output trust, loop limits |
| RAG application | Index poisoning, retrieval leakage across tenants, citation spoofing |
| MCP server | Tool surface, credential custody, confused-deputy flows, consent gaps |
| Infrastructure as code | Public exposure, ingress rules, storage ACLs, key policies, drift |

### Pick a method

| Method | Best for |
|---|---|
| STRIDE per element | Broad first pass over a component diagram |
| STRIDE per interaction | Chatty distributed systems with many hops |
| LINDDUN | Privacy and personal data handling |
| Attack trees | One high-value asset, many paths to it |
| Kill chain walk | Showing how small gaps compose into breach |
| Abuse cases | Product features that can be weaponized against users |
| Trust boundary sweep | Fast triage when time is short |
| Data flow tracing | Following one sensitive field end to end |
| Dependency and supply chain pass | Heavy third-party surface |
| Agent threat pass (injection, tool abuse, autonomy) | Anything with an LLM in the control path |

## Process

1. Scope. Name the repo, the profile, the method, and what is out of bounds. Takes two minutes and prevents most wasted output.
2. Inventory. Agent reads entrypoints, routes, config, IaC, and dependency manifests, then writes the component list with citations.
3. Boundaries. Mark every place data crosses a trust line, including logs and telemetry.
4. Enumerate. Apply the chosen method against the inventory, one component at a time.
5. Rank. Score by reachability first, then impact. Unreachable code ranks low.
6. Fix. Each top finding gets a concrete change: a diff, a config edit, or a task with acceptance criteria.
7. Verify. Pick the top three findings and prove them with a test, a log line, or a manual check.

## Prompt

Paste this into your agent at the repo root. Fill the bracketed fields.


You are an application security engineer doing a threat model of this repository.
You have read access to the codebase. Do not modify files. Do not run network
scans or exploits.

SCOPE
- Repository: [repo name or path]
- Architecture profile: [e.g. LLM agent with tools]
- Threat modeling method: [e.g. STRIDE per interaction]
- Deployment target: [e.g. AWS Lambda behind API Gateway, prod and beta]
- Out of scope: [e.g. the vendored SDK under third_party/, the legacy v1 API]
- Crown jewels: [e.g. customer PII in the orders table, the signing key]

EVIDENCE RULES (hard requirements)
1. Every claim about how the system works cites a file and line range, written
   as `path/to/file.py:120-134`.
2. If you cannot cite it, you may still raise it, but label it `ASSUMPTION` and
   put it in the Assumptions section, not the Findings table.
3. Quote at most 5 lines of code per finding. Point, do not paste the file.
4. Never invent a route, table, env var, IAM action, or dependency. Grep for it
   first. If grep returns nothing, say so.
5. Do not list a threat class that has no matching component. No SQL injection
   section if there is no SQL.
6. Flag contradictions between code and config as findings of their own.

PHASE 1 - INVENTORY
Read entrypoints, route definitions, handlers, auth middleware, config files,
infrastructure as code, Dockerfiles, CI config, and dependency manifests.
Produce:
- Components table: name, purpose, language, entry file:line.
- External dependencies: service, direction, auth mechanism, evidence.
- Data stores: what is stored, sensitivity, encryption at rest, evidence.
- Secrets handling: where credentials come from, evidence.
- Network exposure: every listening socket, published port, ingress rule, and
  storage ACL, with evidence and a note on whether it is public.
- Identity and permissions: roles, policies, scopes, and any wildcard grants.
Stop and print Phase 1 before continuing.

PHASE 2 - TRUST BOUNDARIES
List each boundary where data or control crosses a trust level. For each one
give: the two sides, what crosses, what validates it, and the evidence. Include
logs, metrics, error messages, and background jobs as crossings.

PHASE 3 - ENUMERATION
Apply the chosen method to each component and boundary from Phase 1. For each
finding produce a row with these fields:
- ID (TM-001 and up)
- Title, one line, plain language
- Component and boundary
- Threat category under the chosen method
- Attacker precondition: what access is needed to start
- Mechanism: the concrete steps, 2 to 4 sentences
- Evidence: one or more `path:line` citations
- Impact: what the attacker gains, in business terms
- Reachability: Public / Authenticated / Internal-only / Unreachable, with
  evidence for the claim
- Existing control: what already blocks or slows this, with evidence, or "none
  found"
- Severity: Critical / High / Medium / Low, using the rubric below
- Confidence: High / Medium / Low

If an agent or LLM sits in the control path, run these extra checks and report
each one as found or not found with evidence:
- Untrusted text reaching a model that can call tools
- Tool allowlists and argument validation
- Shell, filesystem, or network reach from tool handlers
- Secrets visible in the model context window
- Loop, cost, and recursion limits
- Model output trusted by downstream code without validation
- Human approval gates on irreversible actions

SEVERITY RUBRIC
- Critical: unauthenticated path to crown-jewel data, remote code execution,
  cross-tenant read or write, or credential theft.
- High: authenticated privilege escalation, broad data exposure, integrity loss
  on a core flow.
- Medium: narrow exposure, needs unusual preconditions, or has partial controls.
- Low: hardening gaps and defense-in-depth items.
Reachability outranks theoretical impact. Unreachable code caps at Low.

PHASE 4 - FIX PLAN
Take the top 10 findings by severity. For each one give:
- The smallest change that removes the threat, as a diff or exact config edit
- Files to touch
- A test or check that proves the fix works
- Effort: hours, days, or weeks
- Any behavior change a user would notice

PHASE 5 - SELF-REVIEW
Before you finish, audit your own output and print the results:
- Count findings. Count citations. Report any finding missing a citation.
- List any claim you made that grep does not support.
- Name the three parts of the system you understand least and say what file,
  document, or person would close the gap.
- Name threat classes you deliberately skipped and why.

OUTPUT
Write the full report to `docs/threat-model-[date].md` with this order:
System summary, Inventory, Trust boundaries, Findings table, Fix plan,
Assumptions, Coverage gaps, Self-review.
Keep the prose plain. No marketing language. No generic security advice that is
not tied to a citation.


## Follow-up prompts

Run these after the first pass, one at a time.

**Prove the top three.** "Take TM-001, TM-002, and TM-003. For each, write a failing test or a manual reproduction procedure that demonstrates the gap in a local or beta environment. Do not touch production. If you cannot demonstrate it, downgrade confidence and say what blocked you."

**Challenge the model.** "You are now a skeptical reviewer who thinks this threat model is padded. Argue against each Critical and High finding. Which ones survive? Which were pattern matching?"

**Deep dive one asset.** "Build an attack tree with [crown jewel] as the root goal. Each leaf needs a `path:line` citation or an `ASSUMPTION` label. Mark which leaves are already blocked."

**Diff since last time.** "Compare this repo against `docs/threat-model-[old date].md`. List findings that were fixed, findings still open, and new components with no coverage. Cite the commits."

**Ticket conversion.** "Turn the fix plan into tickets. One per finding. Title, description with the mechanism and evidence, acceptance criteria, effort estimate. Group by owning component."

## Pitfalls

Agents pad. A 60-finding report with 8 real issues wastes more reviewer time than it saves. The self-review phase and the challenge prompt exist to cut the padding, so run both.

Agents miss what is not in the repo. Runtime config, console-edited IAM policies, load balancer rules, and security group changes made by hand stay invisible. Feed the agent the exported config, or mark those areas as coverage gaps.

Agents over-trust test fixtures. A hardcoded key in a test file is a different problem from one in a handler. Ask for the file path before reacting.

Confidence drops on large repos. For anything past roughly 50k lines, run the skill per service or per bounded context and stitch the reports.

Citations go stale. Pin the commit SHA in the report header, and re-run on any change to auth, routing, IaC, or agent tool definitions.

## Adoption notes

Start with one service you own, the method set to Trust boundary sweep, and a 45-minute budget. Read the output with a colleague and mark each finding real, unclear, or noise. That calibration tells you how much to trust the next run.

Save your filled-in scope block next to the report. The scope block is the reusable part, and rerunning becomes a two-minute job after that.
