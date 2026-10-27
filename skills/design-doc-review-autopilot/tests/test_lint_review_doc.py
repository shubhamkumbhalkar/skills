#!/usr/bin/env python3
"""Tests for lint-review-doc.py using only the Python standard library."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
LINTER = SKILL_DIR / "scripts" / "lint-review-doc.py"


class LintReviewDocTest(unittest.TestCase):
    def run_linter(
        self, markdown: str, banned_terms: str | None = ""
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "document.md"
            document.write_text(markdown, encoding="utf-8")
            command = [sys.executable, str(LINTER), str(document), "--json"]
            if banned_terms is not None:
                terms = root / "terms.txt"
                terms.write_text(banned_terms, encoding="utf-8")
                command.extend(["--banned-terms", str(terms)])
            return subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
            )

    def test_clean_document_passes(self) -> None:
        result = self.run_linter(
            "The publisher validates every submitted record before activation. "
            "Reviewers compare both credible options using the same criteria."
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode)
        self.assertEqual("PASS", report["status"])
        self.assertEqual([], report["errors"])

    def test_punctuation_and_banned_term_fail(self) -> None:
        result = self.run_linter(
            "The first option is ready; however, the second option needs evidence—today.",
            banned_terms="however\n",
        )
        report = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertEqual("FAIL", report["status"])
        error_types = [item["type"] for item in report["errors"]]
        self.assertIn("punctuation", error_types)
        self.assertIn("banned_term", error_types)

    def test_non_prose_regions_are_ignored(self) -> None:
        result = self.run_linter(
            """---
description: however; hidden metadata
---
The reviewer compares both supported options using current evidence.

```java
int retries = 2; // however—valid code
```

Use `value; however—code` from https://example.com/however;token.
<!-- however; hidden comment -->
""",
            banned_terms="however\n",
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode)
        self.assertEqual([], report["errors"])

    def test_indented_fence_inside_list_is_ignored(self) -> None:
        result = self.run_linter(
            """- Example:

    ```bash
    echo "however; hidden—code"
    ```

Reviewers compare the available options using current evidence.
""",
            banned_terms="however\n",
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode)
        self.assertEqual([], report["errors"])

    def test_four_tick_fence_can_contain_three_tick_fence(self) -> None:
        result = self.run_linter(
            """````markdown
```bash
echo "however; hidden—code"
```
````

Reviewers compare the available options using current evidence.
""",
            banned_terms="however\n",
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode)
        self.assertEqual([], report["errors"])

    def test_longer_closing_fence_is_accepted(self) -> None:
        result = self.run_linter(
            """```bash
echo "however; hidden—code"
````

Reviewers compare the available options using current evidence.
""",
            banned_terms="however\n",
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode)
        self.assertEqual([], report["errors"])

    def test_blockquoted_fence_is_ignored(self) -> None:
        result = self.run_linter(
            """> ```bash
> echo "however; hidden—code"
> ```

Reviewers compare the available options using current evidence.
""",
            banned_terms="however\n",
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode)
        self.assertEqual([], report["errors"])

    def test_banned_term_word_boundaries(self) -> None:
        passing = self.run_linter(
            "The delivery plan identifies every reviewer and dependency.",
            banned_terms="very\n",
        )
        failing = self.run_linter(
            "The proposal uses a however-based exception.",
            banned_terms="however\n",
        )
        self.assertEqual(0, passing.returncode)
        self.assertEqual(1, failing.returncode)

    def test_prose_after_fence_is_still_checked(self) -> None:
        result = self.run_linter(
            """```bash
echo safe
```

This prose contains however and must fail.
""",
            banned_terms="however\n",
        )
        report = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertIn("banned_term", [item["type"] for item in report["errors"]])

    def test_bundled_banned_terms_apply_by_default(self) -> None:
        result = self.run_linter(
            "However, reviewers still need direct evidence for this decision.",
            banned_terms=None,
        )
        report = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertIn("banned_term", [item["type"] for item in report["errors"]])

    def test_bundled_terms_work_from_unrelated_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "document.md"
            document.write_text(
                "However, reviewers still need direct evidence for this decision.",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(LINTER), str(document), "--json"],
                cwd=directory,
                check=False,
                capture_output=True,
                text=True,
            )
        report = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertIn("banned_term", [item["type"] for item in report["errors"]])

    def test_banned_terms_can_be_disabled_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "document.md"
            document.write_text(
                "However, reviewers still need direct evidence for this decision.",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(LINTER), str(document), "--no-banned-terms", "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(0, result.returncode)

    def test_missing_banned_terms_file_returns_actionable_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "document.md"
            document.write_text("Reviewers compare both options.", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(LINTER),
                    str(document),
                    "--banned-terms",
                    str(Path(directory) / "missing.txt"),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("banned terms file does not exist", result.stderr)

    def test_long_sentence_produces_warning_without_failure(self) -> None:
        sentence = " ".join(["evidence"] * 31) + "."
        result = self.run_linter(sentence)
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode)
        self.assertIn("long_sentence", [item["type"] for item in report["warnings"]])

    def test_missing_document_returns_actionable_error(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LINTER), "/path/that/does/not/exist.md"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
