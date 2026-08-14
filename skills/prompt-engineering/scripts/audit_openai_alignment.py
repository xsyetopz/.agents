#!/usr/bin/env python3
"""Check prompt-engineering routing and official snapshot provenance.

This is an offline structural audit. It does not refresh remote documentation
or claim that a dated snapshot is still current.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
MANIFEST_PATH = ROOT / "references/official-sources.md"
GENERIC_PATH = ROOT / "references/official/openai-prompt-engineering.2026-08-13.md"
FAMILY_PATH = ROOT / "references/official/openai-gpt-5.6-sol-prompting.2026-08-13.md"
MODEL_PATH = ROOT / "references/official/openai-gpt-5.6-model.2026-08-13.md"

EXPECTED_HASHES = {
    GENERIC_PATH: "ee4459672f1f35c3fc9055e5b44939a99347ce777e406b2c01fbd0760f772fe8",
    FAMILY_PATH: "46181efec9fd1160ef537b0379282a14c1ba32380f2f8149a805128253c1115a",
    MODEL_PATH: "7591e641abc3cb124b2173843a03d40ea05ee421c8a036f04dda44c79188953e",
}

errors: list[str] = []


def require(label: str, condition: bool) -> None:
    if not condition:
        errors.append(label)


try:
    skill = SKILL_PATH.read_text(encoding="utf-8")
    manifest = MANIFEST_PATH.read_text(encoding="utf-8")
    generic = GENERIC_PATH.read_text(encoding="utf-8")
    family = FAMILY_PATH.read_text(encoding="utf-8")
    model = MODEL_PATH.read_text(encoding="utf-8")
except (OSError, UnicodeDecodeError) as exc:
    raise SystemExit(f"prompt-engineering OpenAI alignment audit: FAIL: {exc}") from exc


for path, expected in EXPECTED_HASHES.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    require(
        f"official snapshot hash mismatch: {path.relative_to(ROOT)}", actual == expected
    )

for url in (
    "https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md",
    "https://developers.openai.com/api/docs/guides/prompt-engineering.md",
    "https://developers.openai.com/api/docs/guides/latest-model.md",
):
    require(f"manifest missing official source: {url}", url in manifest)

for phrase in (
    "State each instruction once",
    "Remove one instruction group, example group, or tool at a time",
    "same representative evaluations",
    "Examples are optional",
    "program output and final assistant message",
    "real model or installed agent",
    "paired baseline/candidate behavioral cases",
):
    require(
        f"missing generic workflow guidance: {phrase}", phrase.lower() in skill.lower()
    )

for phrase, source in (
    ("## Prompting current GPT-5 series models", generic),
    ("## Prompting reasoning models", generic),
    ("## Simplify prompts first", family),
    ("## Check work before finishing", family),
    ("latestModelInfo:", model),
):
    require(f"official snapshot missing expected section: {phrase}", phrase in source)

# Keep model routing conditional and prevent the deleted hand-authored guide or
# its obsolete source URLs from silently becoming authority again.
require("GPT-5.6 route is not conditional", "one conditional route" in skill.lower())
require(
    "generic route does not name the official generic snapshot",
    "official/openai-prompt-engineering.2026-08-13.md" in skill,
)
for obsolete in (
    "references/openai-gpt-5.6.md",
    "model-guidance?model=gpt-5.6",
    "prompt-engineering#coding",
):
    require(
        f"obsolete hand-authored/source route remains: {obsolete}",
        obsolete not in skill + manifest,
    )

# Known unsupported or bypass-prone advice must not return to the active core.
for pattern in (
    r"one good example.*ten",
    r"verify once, act once",
    r"one read \+ one grep",
    r"cover 90%",
    r"trust the trigger",
    r"if .*not sure which file.*ask",
    r"if > ?3 negatives",
    r"fix is always: positive reframe",
):
    require(
        f"forbidden generic claim: {pattern}",
        re.search(pattern, skill, re.IGNORECASE | re.DOTALL) is None,
    )

require("skill exceeds lean top-level limit", len(skill.splitlines()) <= 260)

if errors:
    print("prompt-engineering OpenAI alignment audit: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "prompt-engineering OpenAI alignment audit: PASS "
    f"(3 verified official snapshots, {len(skill.splitlines())} SKILL.md lines)"
)
