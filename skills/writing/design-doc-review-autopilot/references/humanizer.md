# Humanizer

Apply these rules while drafting and after every material revision.

## Voice

- Use active voice: `The publisher validates the file` instead of `The file is validated`.
- Prefer concrete subjects and verbs.
- State facts directly, then cite evidence.
- Use plain vocabulary without removing necessary technical terms.
- Explain an acronym on first use when unfamiliar readers are expected.
- Say what is unknown instead of hiding uncertainty behind vague language.

## Sentence and paragraph shape

- Target 10 to 20 words per prose sentence on average.
- Split sentences longer than 30 words unless the structure improves clarity.
- Keep paragraphs focused on one claim or decision.
- Prefer short narrative paragraphs over long bullet inventories.
- Use tables for comparisons, ownership, decisions, and compact contracts.
- Use lists only when order or membership matters.

## Remove mechanical writing

Delete:

- Announcements about what the document will discuss
- Repeated summaries that add no new decision context
- Empty transitions
- Unsupported intensifiers
- Redundant pairs such as `full and complete`
- Vague adjectives when a number or condition is available
- Conclusions that merely repeat the heading

Replace phrases with direct language:

| Avoid | Prefer |
| --- | --- |
| `due to the fact that` | `because` |
| `in order to` | `to` |
| `has the ability to` | `can` |
| `at this point in time` | `now` |
| `a large number of` | a measured count |
| `it should be noted that` | state the fact |

## Punctuation

- Do not use semicolons.
- Do not use em dashes.
- Prefer a period when two claims can stand alone.
- Use parentheses sparingly for short clarifications.

## Evidence language

Use one of these forms:

- `Verified in <source>.`
- `Observed in <measurement>.`
- `Assumption: <claim>.`
- `Evidence required: <test or source>.`
- `Open decision: <choice and owner>.`

Do not write `verified`, `safe`, `atomic`, `idempotent`, or `complete` without naming the mechanism or evidence.

## Configurable banned terms

The bundled `banned-terms.txt` is a strict house style and applies by default. Teams may replace or extend it with `--banned-terms FILE`, or explicitly disable phrase checks with `--no-banned-terms` while keeping punctuation checks.

The linter checks headings, paragraphs, list prose, and table prose. It excludes frontmatter, fenced code, inline code, HTML comments and tags, URLs, and Markdown link targets because technical syntax may contain rejected punctuation or phrases. Indented code without a fence is treated as prose, so technical samples should use fenced code blocks. Do not silently weaken the configured list to make lint pass.

## Final read-aloud check

Read the executive summary, recommendation, option comparison, and requested decisions as if presenting them. Rewrite passages that sound defensive, repetitive, or difficult to say aloud.
