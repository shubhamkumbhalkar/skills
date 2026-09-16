---
name: genai-production-readiness
description: Use when taking an LLM or Generative AI feature to production, or reviewing one. Trigger on "is this GenAI/LLM feature production-ready", "review my LLM pipeline/agent", "ship an AI feature safely", or "what am I missing before launching this AI feature". Checks evals, guardrails, hallucination and prompt-injection mitigation, human-in-the-loop, latency/cost, PII, and observability.
license: MIT
metadata:
  version: "0.1.0"
  author: Shubham Kumbhalkar
---

# GenAI Production Readiness

Evaluate whether an LLM/GenAI feature is safe and reliable to ship. LLM features fail
differently from normal software: they are non-deterministic, can be manipulated by inputs,
and degrade silently. Treat "it works in the demo" as the start, not the finish.

## How to run

1. Restate the feature: the user, the task, the model, what data goes in, and what action
   the output drives (display only vs. takes a real action). The higher the stakes of the
   action, the stricter every check below.
2. Score each area: **Ready / Gap / Blocker**, with the specific risk and the fix.
3. End with a go / no-go and the must-close blockers.

## Checklist

**Evaluation (the #1 gap)**
- Is there an eval set of real inputs with expected outcomes, run automatically?
- Do you measure quality on a rubric, not just vibes? Is there a regression gate before deploy?
- Is there an offline + online (A/B or shadow) signal that quality is holding in production?

**Hallucination & grounding**
- Is output grounded in retrieved/authoritative context (RAG) rather than model memory where facts matter?
- Are claims/citations verifiable? Does the system say "I don't know" instead of inventing?
- Are confidence or source indicators surfaced to the user?

**Guardrails & abuse**
- Prompt-injection defense for any untrusted input (documents, web, user text) that reaches the prompt?
- Output filtering for unsafe/PII/leaking-system-prompt content?
- Can the model trigger tools/actions? If so, are those actions scoped, validated, and reversible?

**Human-in-the-loop**
- For any consequential action (sending, paying, deleting, publishing), is there an approval step?
- Is there a clear "the AI does NOT decide X" boundary, and is it enforced in code, not just prompt?

**Latency, cost & fallbacks**
- p95 latency acceptable? Streaming where it helps UX?
- Per-request and daily cost bounded? Caching where possible? A cap/rate limit against runaway spend?
- Fallback when the model/API is down, slow, or rate-limited (retry, smaller model, cached, or graceful degrade)?

**Privacy & data**
- Is PII minimized before it reaches the model? Is data retention / training-opt-out handled per policy?
- Is prompt/response logging scrubbed of secrets and PII?

**Observability**
- Are inputs, outputs, latency, cost, refusal rate, and guardrail hits logged and dashboarded?
- Can you detect quality drift, a cost spike, or an abuse spike from metrics/alarms?

## Output format

```
## GenAI readiness: <feature>  — <GO | NO-GO>

### Blockers (must close)
1. ...

### Gaps (should close)
- [Evals] risk / fix
- [Guardrails] risk / fix
...

### Ready
- ...
```
