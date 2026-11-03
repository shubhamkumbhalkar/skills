#!/usr/bin/env python3
# Purpose: lint Markdown design documents for mechanical writing patterns.
"""Lint a Markdown design document for mechanical writing patterns.

Usage:
    lint-review-doc.py DOCUMENT [--banned-terms FILE | --no-banned-terms] [--json]

The bundled banned terms file is used by default. Frontmatter, fenced code,
inline code, HTML comments and tags, URLs, and Markdown link targets are
excluded from prose-style checks. Table prose is checked, while inline code
inside a table is excluded.
The script uses only the Python standard library. Errors return exit code 1.
Sentence-length findings are warnings because tables, labels, and technical
expressions can make a strict average misleading.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_MIN_AVERAGE = 10.0
DEFAULT_MAX_AVERAGE = 20.0
DEFAULT_LONG_SENTENCE = 30
DEFAULT_BANNED_TERMS = Path(__file__).resolve().parents[1] / "references" / "banned-terms.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path, help="Markdown document to lint")
    terms_group = parser.add_mutually_exclusive_group()
    terms_group.add_argument(
        "--banned-terms",
        type=Path,
        default=DEFAULT_BANNED_TERMS,
        help="Banned phrases file (default: bundled references/banned-terms.txt)",
    )
    terms_group.add_argument(
        "--no-banned-terms",
        action="store_true",
        help="Disable banned-phrase checks while keeping punctuation checks",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def load_text(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"ERROR: {label} does not exist: {path}")
    except OSError as error:
        raise SystemExit(f"ERROR: cannot read {label} {path}: {error}")


def load_banned_terms(path: Path | None) -> list[str]:
    if path is None:
        return []
    terms = []
    for line in load_text(path, "banned terms file").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            terms.append(value)
    return terms


def mask_match(match: re.Match[str]) -> str:
    """Replace matched content with spaces while preserving line numbers."""
    return mask_string(match.group(0))


def mask_string(value: str) -> str:
    """Replace content with spaces while preserving newlines and offsets."""
    return "".join("\n" if character == "\n" else " " for character in value)


def without_blockquote_prefix(line: str) -> str:
    """Remove Markdown blockquote markers before examining a fence line."""
    return re.sub(r"^[ \t]*(?:>[ \t]*)+", "", line)


def mask_fenced_blocks(markdown: str) -> str:
    """Mask fenced blocks, including indented and blockquoted fences."""
    output: list[str] = []
    fence_character: str | None = None
    minimum_closing_length = 0

    for line in markdown.splitlines(keepends=True):
        candidate = without_blockquote_prefix(line.rstrip("\r\n"))
        fence = re.match(r"^[ \t]*(?P<fence>`{3,}|~{3,})(?P<rest>.*)$", candidate)

        if fence_character is None:
            if fence:
                opening = fence.group("fence")
                fence_character = opening[0]
                minimum_closing_length = len(opening)
                output.append(mask_string(line))
            else:
                output.append(line)
            continue

        output.append(mask_string(line))
        if not fence:
            continue
        closing = fence.group("fence")
        if (
            closing[0] == fence_character
            and len(closing) >= minimum_closing_length
            and not fence.group("rest").strip()
        ):
            fence_character = None
            minimum_closing_length = 0

    return "".join(output)


def lintable_text(markdown: str) -> str:
    """Mask non-prose Markdown regions before punctuation and phrase checks."""
    text = mask_fenced_blocks(markdown)
    patterns = (
        (r"\A---\s*\n.*?\n---\s*(?:\n|$)", re.DOTALL),
        (r"<!--.*?-->", re.DOTALL),
        (r"<[^>\n]+>", 0),
        (r"`[^`\n]*`", 0),
        (r"(?<=\]\()[^)]+(?=\))", 0),
        (r"https?://[^\s)>]+", 0),
    )
    for pattern, flags in patterns:
        text = re.sub(pattern, mask_match, text, flags=flags)
    return text


def prose_only(markdown: str) -> str:
    kept = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            kept.append("")
            continue
        if stripped.startswith(("#", "|", "- ", "* ", ">", "![", "---")):
            continue
        if re.match(r"^\d+\.\s", stripped):
            continue
        kept.append(stripped)
    return "\n".join(kept)


def sentence_word_counts(markdown: str) -> list[tuple[str, int]]:
    prose = prose_only(markdown)
    sentences = re.split(r"(?<=[.!?])\s+|\n+", prose)
    result = []
    for sentence in sentences:
        words = re.findall(r"\b[\w'-]+\b", sentence)
        if words:
            result.append((sentence.strip(), len(words)))
    return result


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def main() -> int:
    args = parse_args()
    markdown = load_text(args.document, "document")
    terms = [] if args.no_banned_terms else load_banned_terms(args.banned_terms)
    lintable = lintable_text(markdown)
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []

    for character, name in ((";", "semicolon"), ("—", "em dash")):
        for match in re.finditer(re.escape(character), lintable):
            errors.append(
                {
                    "type": "punctuation",
                    "value": name,
                    "line": line_number(lintable, match.start()),
                }
            )

    for term in terms:
        pattern = re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)
        for match in pattern.finditer(lintable):
            errors.append(
                {
                    "type": "banned_term",
                    "value": term,
                    "line": line_number(lintable, match.start()),
                }
            )

    counts = sentence_word_counts(lintable)
    average = sum(count for _, count in counts) / len(counts) if counts else 0.0
    if counts and not (DEFAULT_MIN_AVERAGE <= average <= DEFAULT_MAX_AVERAGE):
        warnings.append(
            {
                "type": "average_sentence_length",
                "value": round(average, 1),
                "expected": f"{DEFAULT_MIN_AVERAGE:.0f}-{DEFAULT_MAX_AVERAGE:.0f}",
            }
        )

    for sentence, count in counts:
        if count > DEFAULT_LONG_SENTENCE:
            warnings.append(
                {
                    "type": "long_sentence",
                    "value": count,
                    "preview": sentence[:160],
                }
            )

    report = {
        "document": str(args.document),
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": warnings,
        "sentence_count": len(counts),
        "average_sentence_words": round(average, 1),
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['status']}: {args.document}")
        print(f"Sentences: {len(counts)}, average words: {average:.1f}")
        for item in errors:
            print(f"ERROR line {item['line']}: {item['type']} = {item['value']}")
        for item in warnings:
            detail = item.get("preview", item.get("expected", ""))
            print(f"WARNING: {item['type']} = {item['value']} {detail}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
