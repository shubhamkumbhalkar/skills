---
name: amazon-design-doc-writer
description: "Interactive design document authoring through structured dialogue. Use when writing design docs, one-pagers, or technical proposals that need team review. Guides the user through iterative drafting with self-critique, edge case analysis, and Amazon writing standards."
tags: [skill, writing, design-doc, narrative]
---

# Amazon Design Doc Writer

## Overview

Guides engineers through writing high-quality design documents using an iterative dialogue process. The AI drafts, the human thinks, and together they produce a doc worth reviewing.

## Usage

Use this skill when:
- Writing a design doc, one-pager, or technical proposal
- Preparing a document for team review or decision meeting
- Iterating on an existing draft based on reviewer feedback
- User says "write a design doc", "help me with a one-pager", "draft a proposal"

Do NOT use when:
- Writing runbooks or SOPs (use runbook skills)
- Writing narratives or six-pagers (use amazon-narrative-writing)
- Quick status updates or emails

## Process

### Phase 1: Gather Context

Before writing anything, understand the problem:

1. Ask: "What decision are you trying to drive? Who is the audience?"
2. Ask: "What context does the reader need that they don't already have?"
3. Ask: "What options have you considered? Why did you reject the others?"
4. Ask: "What are the risks? What could go wrong?"
5. Ask: "Are there existing tickets, wikis, or docs I should reference?"

Do NOT start drafting until you have answers to these questions. The thinking happens here, not in the writing.

### Phase 2: Draft

Write the first draft with these sections (adapt as needed):

- **Current State** — what exists today, with links to resources
- **Problem** — what is broken or missing, with evidence (tickets, incidents, data)
- **Requirements** — what the solution must do, stated as outcomes not tools
- **Options** — at least two approaches with honest pros and cons
- **Recommendation** — which option and why, with clear reasoning
- **Observability** — how you detect when things go wrong
- **Risks** — what could fail and how you mitigate
- **Next Steps** — concrete actions with owners

After drafting, tell the user: "Read through this. Come back with your questions, disagreements, or things that feel unclear. We'll iterate until you're confident in every sentence."

### Phase 3: Dialogue and Critique

This is where the real value happens. For each round of feedback:

1. Answer the user's questions with specifics (data, links, evidence)
2. Challenge assumptions: "Why this timeout value? What happens if it's too short?"
3. Surface edge cases: "What if the upstream is down for a week?"
4. Ask: "Would you bet your oncall pager on this design?"
5. Update the draft and present the changes clearly

Repeat until the user is ready to share with the team.

### Phase 4: Reviewer Feedback

When the user brings comments from reviewers:

1. Parse each comment and provide a clear answer
2. Identify which comments require doc changes vs verbal responses
3. Update the draft to address structural feedback
4. Flag comments that challenge the recommendation — help the user decide if the recommendation should change

## Writing Standards

### Structure
- State the purpose in the first paragraph
- End with a recommendation and next steps
- Keep the main body under 6 pages (appendices excluded)
- Use headings to guide the reader through the narrative

### Language
- Active voice over passive: "We chose X" not "X was chosen"
- Simple words over jargon: "call the API" not "invoke the service endpoint"
- Specific over vague: "34 billion rows" not "a large dataset"
- No m-dashes. Use commas or restructure the sentence.
- Expand acronyms on first use: "Wait For Dependencies (WFD)"
- No weasel words: replace "significant", "soon", "might" with data or commitments

### Conciseness Checklist
- Remove redundant pairs ("full and complete" → "complete")
- Remove unnecessary qualifiers ("actually", "really", "basically")
- Replace phrases with words ("due to the fact that" → "because")
- Cut sentences that repeat what the previous sentence said
- Don't announce what you're going to do. Just do it. ("I want to point out that" → delete)

### Data and Evidence
- Link to tickets, wikis, and code when referencing them
- Use numbers instead of adjectives: "60,000 merchants" not "many merchants"
- Reference existing implementations when proposing patterns
- Include resource links (profiles, tables, pipelines) so readers can verify

### Formatting
- Spell out acronyms on first use
- Use bullet lists only for actual lists, not for prose
- Hyperlink references inline, don't dump URLs at the end
- White space between sections

## Anti-Patterns

### The AI-Generated Template
A doc that is structurally correct but has no original thinking. Every section reads like a fill-in-the-blank. The user hasn't wrestled with the tradeoffs.

**Fix:** Phase 3 (dialogue) is mandatory. The AI should challenge the user's decisions and surface gaps. If the user can't defend a choice, the doc isn't ready.

### The Kitchen Sink
A doc that includes every detail because the author isn't sure what matters. Overwhelms the reader and buries the key decisions.

**Fix:** For every paragraph, ask "why does the reader care?" If the answer is "context" but the reader already has it, cut it. Move deep details to appendices.

### The Missing Alternative
A doc that proposes one solution without seriously evaluating others. Reviewers will ask "what else did you consider?" and the author won't have an answer.

**Fix:** Present at least two options with honest pros and cons. It's okay to have a clear recommendation, but the reader should understand why the alternatives were rejected.

### The Jargon Wall
A doc that uses internal tool names, acronyms, and system names without context. Only readable by people who already know the answer.

**Fix:** Assume the reader is smart but unfamiliar with your specific tools. Expand acronyms, explain what systems do (one sentence), and link to docs.

## Mentor Guidance

The goal of writing is not the words. It is the clarity of thought that comes from wrestling with the problem. AI should augment this process, not replace it.

Encourage the user to:
- Read their own draft critically before sharing
- Ask themselves "would I bet my oncall pager on this?"
- Challenge their own assumptions before reviewers do
- Use the dialogue process to sharpen their thinking, not just polish prose
- Iterate multiple rounds — the first draft is never the final doc

When the user asks for a full rewrite, provide it, but always follow up with: "Read through this. Come back with what feels off. This is a starting point, not the final version."
