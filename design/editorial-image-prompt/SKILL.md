---
name: editorial-image-prompt
description: Generate a featured-image prompt that is specific to one article and varied across a style kit, instead of the same generic AI header every time. Use when you need a text-to-image prompt for a blog or newsletter header, or when your auto-generated images keep looking the same. Reads the article, invents a fresh visual metaphor, and renders it in a rotating handmade editorial style.
tags: [design, image-prompt, editorial, blog, content, text-to-image]
---

# Editorial Image Prompt

## Overview

Auto-generated blog images go stale two ways. They repeat the same scene (a developer at a
desk, a robot, glowing nodes), and they repeat the same style. This skill fixes both. It
reads the actual article, finds a fresh visual metaphor for that specific piece, and renders
it in a style drawn from a rotating kit, so headers stay on-topic and keep varying.

The output is a text-to-image prompt you paste into an image generator. It never generates
the image itself.

## Usage

Use when:
- You need a featured or header image prompt for a specific article or post.
- Your automated pipeline keeps producing near-identical image prompts week after week.

Do not use for:
- Logos, icons, or data figures that must be accurate (use a real chart tool for data).

## Process (two steps)

**Step 1, find the metaphor.** Read the article. Write down its single central idea and 2-3
concrete things it discusses. Invent ONE visual metaphor for that specific idea. Hard rule:
do not use a developer at a desk, a laptop, a robot, a brain, a lightbulb, or a network of
glowing nodes. The metaphor must be specific to this article, the way an editorial
illustrator finds an image that carries the argument.

**Step 2, compose the prompt.** Fill four slots:
- SUBJECT: the metaphor scene, concrete and specific.
- STYLE: this week's style from the kit below (round-robin, see Selection).
- COMPOSITION: 16:9, with clear negative space on one side for a headline overlay.
- MOOD: fitting the article's argument.

Then apply the constraints.

## Style kit (round-robin)

Pick by a rotating index so no two consecutive posts share a style. In a scheduled pipeline,
index by ISO week number modulo the kit size.

1. Editorial ink-line illustration, loose pen-and-ink, visible linework, paper grain (New Yorker or Economist feel).
2. Risograph print, two or three spot inks with slight registration offset, halftone dots, zine texture.
3. Linocut relief print, bold carved lines, high contrast, gouge marks, one or two ink colors on rough paper.
4. Cut-paper collage, layered torn and cut shapes with real edges and soft shadows, limited paper-stock palette.
5. Technical blueprint schematic, hand-annotated drafting lines on cyanotype-blue, diagrammatic.
6. Mid-century modern flat, 1950s-60s editorial, geometric simplified shapes, muted palette, slight print texture.
7. Editorial gouache painting, visible brush texture, matte flat washes, hand-painted edges.
8. Duotone halftone screenprint, two colors, Ben-Day dots, bold poster composition.
9. Abstract data-as-art, bars, lines, and grids arranged as a composition, hand-rendered not corporate, paper texture.

All are handmade or editorial. Avoid 3D render, claymation, and photoreal, which read as
AI-generated.

## Constraints (keep it from looking AI)

- Depict the article's own metaphor as a concrete scene with real subjects. Never an abstract
  network of glowing nodes.
- Do not default to a developer at a desk, a laptop, a robot, a brain, or a lightbulb. Vary
  the scene every time.
- Commit to the named medium and make its texture visible. Avoid the over-clean, plastic,
  evenly-lit look.
- Limited palette, two or three named colors. No rainbow gradients.
- 16:9, negative space on one side for a headline.
- Banned in the image: text, letters, numbers, logos, circuit boards, HUD interfaces, gears,
  rocket ships, robots with glowing eyes, generic digital-blue gradients.

## Output

Return the final text-to-image prompt. If you reason in two steps, return JSON
`{"metaphor": "...", "image_prompt": "..."}` so the metaphor is auditable.
