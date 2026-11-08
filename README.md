# Shubham Kumbhalkar — Agent Skills

A small, high-signal collection of Agent Skills for building and reviewing large-scale
backend systems, distilled from 10+ years shipping distributed systems and applied AI in
production (systems processing $48B+/yr at 99.99% uptime).

Compatible with Claude Code, Codex, Cursor, and the open [Agent Skills standard](https://agentskills.io).

## Install

```bash
npx skills add shubhamkumbhalkar/skills
```

Pick the skills you want and the agent(s) to install them on. To grab a single skill:

```bash
npx skills add shubhamkumbhalkar/skills --skill distributed-systems-design-review
```

## Skills

Organized by category under `skills/<category>/<name>/`. Install any one by name (the
`--skill` flag matches the skill's name, wherever it lives in the tree):

```bash
npx skills add shubhamkumbhalkar/skills --skill distributed-systems-design-review
```

**architecture**
| Skill | Use it when |
|---|---|
| **distributed-systems-design-review** | Reviewing a system design / RFC / PR for reliability and correctness at scale (idempotency, retries, backpressure, consistency, failure modes, observability). |
| **zero-downtime-migration** | Planning or reviewing a zero-downtime migration of a live/Tier-1 service or datastore (dual-write, backfill, shadow, phased cutover, rollback). |
| **change-safety** | Before any change that is hard to reverse or touches a shared/production system (CR, deploy, pipeline promote, manual CLI/infra command, resource delete): researches how the change is actually applied, pre-mortems the failure modes and recovery, and forces a safer-alternative check before acting. |

**ai**
| Skill | Use it when |
|---|---|
| **genai-production-readiness** | Taking an LLM/GenAI feature to production (guardrails, evals, hallucination + prompt-injection mitigation, human-in-the-loop, latency/cost, PII, observability). |
| **time-series-forecasting-review** | Building or reviewing a forecasting model/pipeline (demand, capacity, revenue): data leakage, valid backtesting, baselines, seasonality/covariates, metrics, and drift. |

**security**
| Skill | Use it when |
|---|---|
| **evidence-traced-threat-model** | Point an agent at a repo and get a threat model where every finding cites a file and line. |

**writing**
| Skill | Use it when |
|---|---|
| **amazon-design-doc-writer** | Writing a design doc, one-pager, or technical proposal that needs team review. |
| **design-doc-review-autopilot** | Drafting, humanizing, visualizing, and reviewing technical designs with bounded critic panels. |
| **humanizer** | Rewriting or drafting prose so it reads human, not AI: strips em dashes and buzzwords, shortens sentences, forces concrete facts. |

**productivity**
| Skill | Use it when |
|---|---|
| **portable-agent-skills-library** | Turning repeated agent instructions into reusable SKILL.md files that work across Claude Code and Codex. |



**design**
| Skill | Use it when |
|---|---|
| **editorial-image-prompt** | Generating a featured-image prompt that is specific to one article and varied across a style kit, instead of the same generic AI header every time. |

Categories: `architecture`, `ai`, `security`, `writing`, `productivity`, `devtools`, `design`.

## Why these

They encode the review discipline I actually use on Tier-1 systems, not generic advice.
Each skill is a checklist-driven workflow an agent can follow to catch the failure modes
that cause real production incidents.

## About

Built by **Shubham Kumbhalkar**, a software engineer focused on distributed systems,
cloud platforms, and applied Generative AI.
- Portfolio: https://shubhamkumbhalkar.github.io
- LinkedIn: https://www.linkedin.com/in/shubham-kumbhalkar/

Contributions and issues welcome.

## License

MIT
