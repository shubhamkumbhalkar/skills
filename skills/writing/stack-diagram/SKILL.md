---
name: stack-diagram
description: Turn a one-sentence description of a tech stack into an architecture diagram that uses the official logos of each service, rendered as Mermaid or SVG and saved next to your docs. Use when writing a README, a design doc, an onboarding page, or a slide that needs a picture of the system.
tags: [documentation, diagrams, architecture, mermaid, svg, developer-productivity, readme]
---

# Stack Diagram

## Overview

You describe a system in plain words: "Next.js frontend on Vercel, FastAPI on ECS Fargate behind an ALB, Aurora Postgres, Redis cache, S3 for uploads, Bedrock for the LLM calls." The skill produces an architecture diagram where each node carries that product's real logo, grouped by layer and connected by labeled edges. Output is a text file you commit, so the diagram lives in git and changes show up in code review.

Two output modes:

- **Mermaid** (`architecture-beta` or `flowchart` with `iconify` logos). Renders inline on GitHub, GitLab, and most wikis. Best default.
- **Standalone SVG** with embedded logo images. Best for slides, Quip, and anywhere Mermaid is not rendered.

Logos come from public icon sets, mostly Iconify `logos:` and `simple-icons:`, plus the AWS architecture icon set for AWS services. The skill never invents an icon name it has not checked, and it never hotlinks a random image from a search result.

## Usage

### When to use

- A README or design doc has a paragraph describing the system and no picture.
- You are about to hand-draw boxes in draw.io for the fourth time this quarter.
- An onboarding page needs a "how requests flow" diagram that a new hire can read in 20 seconds.
- A design review needs a before and after diagram of the same stack.
- You want the diagram in version control so a stack change shows up as a diff.

### When not to use

- You need a precise network topology with subnets, route tables, and security group rules. Use a real diagram tool or Infrastructure Composer for that.
- You need an exact replica of an existing hand-made diagram. This skill composes a fresh one.
- The logos matter legally, for example a customer-facing marketing asset. Trademark use rules apply and you should check with the brand owner.
- The system has more than roughly 25 components. Split it into per-domain diagrams first.

### Cost and limits

Mermaid `architecture-beta` is still beta, so syntax shifts between Mermaid versions. Pin the version you tested against in the doc, or fall back to `flowchart` with `@{ icon: ... }` nodes, which has been stable longer. GitHub renders a subset of Mermaid features, so always open the rendered file once before you ship it.

## Process

1. **Collect the stack.** Read the user's sentence. If a layer is missing, ask one question at most, then assume the common choice and say what you assumed. Do not interview the user.
2. **Normalize the component names.** Map each phrase to a canonical product name: "postgres on RDS" becomes "Amazon Aurora PostgreSQL", "the queue" becomes "Amazon SQS" if the rest of the stack is AWS.
3. **Resolve a logo per component.** Prefer `logos:<slug>` from Iconify, then `simple-icons:<slug>`, then the AWS architecture icon for AWS services. If no logo exists, use a plain labeled box. Never guess a slug. Check it against the Iconify search API or the local icon set before you emit it.
4. **Group into layers.** Client, edge, compute, data, async, external. Put each group in a Mermaid `group` or `subgraph`.
5. **Draw the request path.** One primary path from client to datastore, labeled with the protocol: HTTPS, gRPC, SQL, S3 API. Secondary paths dashed.
6. **Emit the file.** Write `docs/architecture.md` with the Mermaid block, or `docs/architecture.svg` for the standalone mode. Keep the source sentence in a comment at the top so the next person can regenerate it.
7. **Verify.** Run the Mermaid CLI or render the SVG and confirm every node has a visible logo and no edge crosses a group boundary twice. Report any component that fell back to a plain box.

## Prompt

Paste this, then your stack sentence.


You are generating an architecture diagram from a one-sentence stack description.

STACK: <one or two sentences describing the system>
OUTPUT: mermaid        # or: svg
TARGET: github         # or: gitlab, quip, slides, confluence
FILE: docs/architecture.md

Do this:

1. List every component you detected from STACK, one per line, as
   `detected name -> canonical product name -> layer`.
   Layers: client, edge, compute, data, async, external, observability.
   If STACK is missing a layer that the system clearly needs, add it and mark
   it ASSUMED. Do not ask me questions unless two readings of STACK give
   different systems.

2. For each component, resolve one icon. Order of preference:
     a. Iconify `logos:<slug>`   (full-color brand logos)
     b. Iconify `simple-icons:<slug>`  (monochrome)
     c. AWS architecture icon name, for AWS services
     d. no icon, plain labeled box
   You must not emit an icon slug you have not verified exists. If you cannot
   verify, drop to option d and say so. List the resolutions as
   `component -> icon slug -> source`.

3. Emit the diagram.

   For OUTPUT=mermaid, use `architecture-beta` when TARGET renders it, else
   use `flowchart LR` with icon nodes:
     N1@{ icon: "logos:nextjs", form: "square", label: "Next.js" }
   Rules:
     - One subgraph or group per layer, labeled.
     - Left to right. Client on the left, data on the right.
     - Label every edge with its protocol (HTTPS, gRPC, SQL, S3 API, event).
     - Solid line for the main request path, dashed for async and telemetry.
     - No more than 25 nodes. If STACK implies more, split into two diagrams
       and name them by domain.

   For OUTPUT=svg, emit one self-contained SVG:
     - viewBox sized to content, no fixed width or height.
     - Each logo as an <image> with a data: URI, or an <use> from an inline
       <defs> symbol set. No external URLs, so the file works offline.
     - Text in a system font stack, 14px labels, 12px edge labels.
     - Layer bands as rounded rects with a 10% tint, labels top-left.

4. Write the file at FILE. Put this header comment at the top, inside the
   file's comment syntax:
     generated from: <the STACK sentence, verbatim>
     regenerate with: stack-diagram skill
     assumed: <comma separated ASSUMED components, or "none">

5. Report back, short:
     - components drawn, and which ones fell back to a plain box
     - which assumptions you made
     - the one command I should run to see it rendered

Constraints:
  - Never invent a product name that is not in STACK or a direct consequence
    of it. If STACK says "a queue" and the stack is AWS, SQS is fine. If the
    cloud is unknown, write "Message queue" with no logo.
  - Never hotlink an image from a web search. Icons come from a named icon set
    or a data URI you embedded.
  - Keep the diagram readable at 800px wide. Drop detail before you shrink text.


### Variant: before and after

For a migration doc, run the prompt twice with `STACK` set to the current and target systems, then ask for a third pass:


Given the two diagrams above, emit a third Mermaid diagram showing only what
changes: components removed (dashed red), added (solid green), unchanged
(grey, no logo). Add a two-column table listing each change and its reason,
with the reason left blank for me to fill in.


### Variant: trust boundaries

Useful for a security review, which is where a stack diagram earns its keep.


Re-emit the diagram with trust boundaries drawn as dashed rectangles:
public internet, VPC public subnet, VPC private subnet, AWS managed service,
third party. Label every edge that crosses a boundary with its auth mechanism
(SigV4, OIDC, mTLS, API key, none). Any edge you label "none" gets a red
marker and a line in a findings list below the diagram.


## Checks before you ship

- Open the rendered file. GitHub silently drops Mermaid features it does not support, and a broken block shows as raw text.
- Confirm every logo is the right product. A wrong logo in a design doc is worse than no logo.
- Check the header comment holds the original sentence, so the diagram can be regenerated without you.
- If the diagram is in a customer-facing asset, check trademark use with the brand owner before publishing.
