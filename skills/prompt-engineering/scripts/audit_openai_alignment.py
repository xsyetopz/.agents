#!/usr/bin/env python3
"""Static source and structure audit for the prompt-engineering skill."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
OPENAI = (ROOT / "references/openai-gpt-5.6.md").read_text(encoding="utf-8")
MODEL = (ROOT / "references/model-reasoning-guide.md").read_text(encoding="utf-8")
TEMPLATES = (ROOT / "references/prompt-templates.md").read_text(encoding="utf-8")
CORE = "\n".join((SKILL, OPENAI, MODEL, TEMPLATES))

errors: list[str] = []

def require(label: str, condition: bool) -> None:
    if not condition:
        errors.append(label)

# Source authority and full clause inventory.
for url in (
    "https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6",
    "https://developers.openai.com/api/docs/guides/prompt-engineering#coding",
):
    require(f"missing official source: {url}", url in OPENAI)
clause_ids = set(re.findall(r"\| (OAI-[A-Z]+-\d+) \|", OPENAI))
require("official clause matrix is incomplete", len(clause_ids) >= 20)

# OpenAI's central lean-prompt and evaluation requirements.
for phrase in (
    "State each instruction once",
    "Remove one instruction group, example group, or tool at a time",
    "same representative evaluations",
    "Examples are optional",
    "program output and final assistant message",
    "real model or installed agent",
    "paired baseline/candidate rollouts",
):
    require(f"missing required guidance: {phrase}", phrase.lower() in CORE.lower())

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
    require(f"forbidden generic claim: {pattern}", re.search(pattern, CORE, re.I | re.S) is None)

# The active model guide must not carry unsourced benchmark/model-catalog facts.
for pattern in (r"SWE-bench", r"AA Index", r"\bt/s\b", r"\d+B active", r"1,000,000 tokens"):
    require(f"unsupported model-table claim remains: {pattern}", re.search(pattern, MODEL, re.I) is None)

# The compact authority policy appears once in the coding template and once as
# the skill's documented example; prose elsewhere must refer to it, not clone it.
require("skill has duplicate Autonomy and approval headings", SKILL.count("### 3. Define autonomy and approval once") == 1)
require("template has duplicate Autonomy and approval headings", TEMPLATES.count("# Autonomy and approval") == 1)
require("skill exceeds lean top-level limit", len(SKILL.splitlines()) <= 260)
require("model guide exceeds lean reference limit", len(MODEL.splitlines()) <= 100)

if errors:
    print("prompt-engineering OpenAI alignment audit: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"prompt-engineering OpenAI alignment audit: PASS ({len(clause_ids)} clauses, {len(SKILL.splitlines())} SKILL.md lines)")
