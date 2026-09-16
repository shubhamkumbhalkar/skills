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

| Skill | Use it when |
|---|---|
| **distributed-systems-design-review** | Reviewing a system design / RFC / PR for reliability and correctness at scale (idempotency, retries, backpressure, consistency, failure modes, observability). |
| **zero-downtime-migration** | Planning or reviewing a zero-downtime migration of a live/Tier-1 service or datastore (dual-write, backfill, shadow, phased cutover, rollback). |
| **genai-production-readiness** | Taking an LLM/GenAI feature to production (guardrails, evals, hallucination + prompt-injection mitigation, human-in-the-loop, latency/cost, PII, observability). |

## Why these

They encode the review discipline I actually use on Tier-1 systems, not generic advice.
Each skill is a checklist-driven workflow an agent can follow to catch the failure modes
that cause real production incidents.

## About

Built by **Shubham Kumbhalkar**, Software Development Engineer II at Amazon — distributed
systems, cloud platforms, and applied Generative AI.
- Portfolio: https://shubhamkumbhalkar.github.io
- LinkedIn: https://www.linkedin.com/in/shubham-kumbhalkar/

Contributions and issues welcome.

## License

MIT
