# Visual Guide

Use diagrams to replace explanation, not decorate it.

## Visual set

Choose the smallest useful set:

1. **Current state:** Show the existing request and data path.
2. **One diagram per credible option:** Give every option equal visual weight.
3. **Selected sequence:** Add only when ordering, activation, or consistency matters.
4. **Failure and rollback:** Add only when recovery crosses multiple systems.
5. **Measurement:** Add only when the baseline, treatment, actuals, and reporting joins are hard to explain in prose.

A 30-minute companion usually needs the current state and one diagram per option. Keep deeper sequence and recovery visuals in the full design.

## Meeting-friendly option diagrams

- Use a left-to-right flow with five to seven nodes.
- Keep each node to one concept and one or two short lines.
- Use the same height, font, colors, direction, and level of detail for every option.
- Target a compact strip that fits without scrolling. A height near 65 to 160 pixels usually works for a short review, depending on the renderer.
- Add one sentence below the diagram stating the decision consequence.
- Place pros and cons immediately after the visual.

The agent MUST NOT make the recommended option larger or more polished because unequal presentation biases reviewers.

## Full-design diagrams

A full design MAY use larger diagrams when it needs to show:

- State ownership and trust boundaries
- Write order and activation points
- Retry, failure, and rollback paths
- Migration or coexistence phases
- Measurement joins and missing-data branches

Keep diagrams under ten primary nodes. Split topology and sequence when one image becomes dense.

## Visual content rules

Every diagram SHOULD answer one question:

- What exists today?
- How does this option work?
- Where does state live?
- What happens after failure?
- How is success measured?

Use labels that name responsibilities rather than internal implementation trivia. Use arrows with a clear direction. Mark asynchronous boundaries, sources of truth, human approval, and irreversible side effects when relevant.

## Rendering and accessibility

The agent MUST:

- Render each diagram before embedding it
- Inspect dimensions, clipping, alignment, contrast, and text size
- Use meaningful alt text
- Keep source files when the output may need revision
- Verify that image links work for the intended audience
- Remove private names, identifiers, and screenshots from public versions

The agent MUST NOT rely on source markup alone because valid diagram code can still render poorly.

## Common visual mistakes

- **Unequal options:** One option has a polished architecture while another has a sentence.
- **Narration duplicates the picture:** The caption should state the consequence, not list every box.
- **One diagram does everything:** Split current state, options, and recovery.
- **Tiny unreadable text:** Reduce nodes before reducing font size.
- **Decorative icons:** Use them only when they improve scanning.
- **Leaking private context:** Recreate a clean diagram instead of using a screenshot.
