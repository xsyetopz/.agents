#!/usr/bin/env python3
"""Validate the copied package contract without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HEADINGS = [
    "Use this skill",
    "Rules",
    "Steps",
    "Resources",
    "Verify",
]
EXPECTED_FILES = [
    "SKILL.md",
    "LICENSE",
    ".skill-validator.json",
    "agents/openai.yaml",
    "references",
    "assets/contract.json",
    "evals/evals.json",
    "scripts/check.py",
]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
FENCE_RE = re.compile(r"^[ \t]*(```|~~~)")
FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]*(.*))?$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

# Build host-path markers from fragments so this checker contains no forbidden
# machine-specific path of its own when it scans the complete package tree.
GLOBAL_RE = re.compile(
    r"(?<![A-Za-z0-9_/])(?:"
    + "|".join(
        re.escape(marker)
        for marker in (
            "/" + "Users/",
            "/" + "home/",
            "/" + "root/",
            "/" + "private/" + "tmp/",
            "/" + "tmp/",
            "~" + "/.agents/",
            "~" + "/.codex/",
            "$" + "HOME/",
            "C:" + "\\\\Users\\\\",
        )
    )
    + r")"
)


def add(errors: list[str], message: str) -> None:
    errors.append(message)


def read_text(path: Path, errors: list[str], label: str | None = None) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        add(errors, f"{label or path.relative_to(ROOT)}: cannot read ({exc})")
        return None


def load_json(path: Path, errors: list[str]) -> object | None:
    text = read_text(path, errors)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        add(errors, f"{path.relative_to(ROOT)}: invalid JSON ({exc.msg})")
        return None


def package_path(value: object, errors: list[str], label: str) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        add(errors, f"{label}: expected a non-empty package-relative path")
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        add(errors, f"{label}: path escapes package ({value!r})")
        return None
    try:
        target = (ROOT / relative).resolve()
        target.relative_to(ROOT.resolve())
    except (OSError, RuntimeError, ValueError):
        add(errors, f"{label}: path escapes package ({value!r})")
        return None
    return target


def parse_frontmatter(text: str, errors: list[str]) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        add(errors, "SKILL.md: frontmatter must start on line 1")
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        add(errors, "SKILL.md: frontmatter closing delimiter is missing")
        return {}, text
    fields: dict[str, str] = {}
    for line_no, line in enumerate(lines[1:end], 2):
        if not line.strip():
            continue
        match = FIELD_RE.match(line)
        if not match:
            add(errors, f"SKILL.md:{line_no}: malformed frontmatter field")
            continue
        key, value = match.group(1), (match.group(2) or "").strip()
        if key in fields:
            add(errors, f"SKILL.md:{line_no}: duplicate frontmatter field {key!r}")
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            add(errors, f"SKILL.md:{line_no}: block frontmatter values are unsupported")
        fields[key] = value.strip("\"'")
    return fields, "\n".join(lines[end + 1 :])


def _linked_package_paths(source: Path, text: str, errors: list[str]) -> set[str]:
    """Resolve links from one Markdown file to package-relative paths."""
    mapped: set[str] = set()
    for match in LINK_RE.finditer(text):
        target = match.group(1).split("#", 1)[0].split("?", 1)[0].strip()
        if not target or target.startswith(
            ("http://", "https://", "mailto:", "#", "//")
        ):
            continue
        candidate = (source.parent / target).resolve()
        try:
            relative = candidate.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            add(errors, f"{source.relative_to(ROOT)}: link leaves package ({target})")
            continue
        if not candidate.exists():
            add(errors, f"{source.relative_to(ROOT)}: broken local link ({target})")
            continue
        mapped.add(relative)
    return mapped


def check_skill(errors: list[str], contract: dict[str, object]) -> None:
    path = ROOT / "SKILL.md"
    text = read_text(path, errors, "SKILL.md")
    if text is None:
        return
    frontmatter, body = parse_frontmatter(text, errors)
    name = frontmatter.get("name", "")
    if not name or not NAME_RE.fullmatch(name):
        add(errors, "SKILL.md: name must be lowercase hyphenated text")
    if name != ROOT.name:
        add(errors, f"SKILL.md: name {name!r} does not match package {ROOT.name!r}")
    if not frontmatter.get("description", "").strip():
        add(errors, "SKILL.md: description must be non-empty")

    headings: list[tuple[int, str]] = []
    fenced = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((len(match.group(1)), match.group(2).strip()))
    level_one = [title for level, title in headings if level == 1]
    sections = [title for level, title in headings if level == 2]
    if len(level_one) != 1:
        add(errors, "SKILL.md: require exactly one level-one title")
    if sections != EXPECTED_HEADINGS:
        add(
            errors,
            f"SKILL.md: level-two headings must be {EXPECTED_HEADINGS!r}; got {sections!r}",
        )
    mapped = _linked_package_paths(path, body, errors)
    index = ROOT / "references" / "index.md"
    index_text = read_text(index, errors, "references/index.md")
    if index_text is not None:
        mapped.update(_linked_package_paths(index, index_text, errors))
    reference_paths = contract.get("reference_paths")
    if not isinstance(reference_paths, list):
        return
    for reference in reference_paths:
        if isinstance(reference, str) and reference not in mapped:
            add(
                errors,
                f"SKILL.md or references/index.md does not route contract reference ({reference})",
            )


def check_openai(errors: list[str]) -> None:
    path = ROOT / "agents" / "openai.yaml"
    text = read_text(path, errors, "agents/openai.yaml")
    if text is None:
        return
    if not re.search(r"(?m)^interface:\s*$", text):
        add(errors, "agents/openai.yaml: missing interface mapping")
    for field in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf"(?m)^\s+{field}:\s*\S", text):
            add(errors, f"agents/openai.yaml: missing {field}")
    match = re.search(r"(?m)^\s+default_prompt:\s*(.+)$", text)
    if not match:
        return
    prompt = match.group(1).strip().strip("\"'")
    tokens = re.findall(r"\$[A-Za-z0-9-]+", prompt)
    expected = "$" + ROOT.name
    if tokens != [expected]:
        add(
            errors, f"agents/openai.yaml: default_prompt must invoke exactly {expected}"
        )


def check_validator(errors: list[str]) -> None:
    path = ROOT / ".skill-validator.json"
    payload = load_json(path, errors)
    if not isinstance(payload, dict):
        add(errors, ".skill-validator.json: expected an object")
        return
    headings = payload.get("required_headings")
    if (
        not isinstance(headings, list)
        or [str(item).lstrip("# ") for item in headings] != EXPECTED_HEADINGS
    ):
        add(
            errors,
            ".skill-validator.json: required_headings must cover the common headings in order",
        )
    required = payload.get("required_files")
    if not isinstance(required, list):
        add(errors, ".skill-validator.json: required_files must be an array")
        return
    for index, value in enumerate(required):
        target = package_path(
            value, errors, f".skill-validator.json required_files[{index}]"
        )
        if target is not None and not target.is_file():
            add(errors, f".skill-validator.json required file is missing: {value}")


def check_contract(errors: list[str]) -> dict[str, object]:
    payload = load_json(ROOT / "assets" / "contract.json", errors)
    if not isinstance(payload, dict):
        add(errors, "assets/contract.json: expected an object")
        return {}
    if payload.get("schema_version") != 1:
        add(errors, "assets/contract.json: schema_version must be 1")
    if payload.get("skill_name") != ROOT.name:
        add(errors, "assets/contract.json: skill_name must match package")
    if payload.get("required_headings") != EXPECTED_HEADINGS:
        add(
            errors,
            "assets/contract.json: required_headings do not match the common contract",
        )
    if payload.get("required_files") != EXPECTED_FILES:
        add(
            errors,
            "assets/contract.json: required_files do not match the common contract",
        )
    for index, value in enumerate(payload.get("required_files", [])):
        target = package_path(
            value, errors, f"assets/contract.json required_files[{index}]"
        )
        if target is not None:
            expected_kind = (
                target.is_dir() if value == "references" else target.is_file()
            )
            if not expected_kind:
                add(errors, f"assets/contract.json required file is missing: {value}")
    references = payload.get("reference_paths")
    if not isinstance(references, list) or not references:
        add(errors, "assets/contract.json: reference_paths must be a non-empty array")
    else:
        for index, value in enumerate(references):
            target = package_path(
                value, errors, f"assets/contract.json reference_paths[{index}]"
            )
            if isinstance(value, str) and not value.startswith("references/"):
                add(
                    errors,
                    f"assets/contract.json reference_paths[{index}]: must stay under references/",
                )
            if target is not None and not target.is_file():
                add(errors, f"assets/contract.json reference is missing: {value}")
    case_ids = payload.get("eval_case_ids")
    if (
        not isinstance(case_ids, list)
        or len(case_ids) < 3
        or any(not isinstance(item, str) or not item.strip() for item in case_ids)
    ):
        add(
            errors,
            "assets/contract.json: eval_case_ids needs at least three non-empty strings",
        )
    elif len(set(case_ids)) != len(case_ids):
        add(errors, "assets/contract.json: eval_case_ids must be unique")
    return payload


def check_evals(errors: list[str], contract: dict[str, object]) -> None:
    path = ROOT / "evals" / "evals.json"
    payload = load_json(path, errors)
    if not isinstance(payload, dict):
        add(errors, "evals/evals.json: expected an object")
        return
    if payload.get("schema_version") != 1:
        add(errors, "evals/evals.json: schema_version must be 1")
    if payload.get("skill_name") != ROOT.name:
        add(errors, "evals/evals.json: skill_name must match package")
    static = payload.get("static")
    if not isinstance(static, list):
        add(errors, "evals/evals.json: static must be an array")
    elif not any(
        isinstance(item, dict)
        and item.get("id") == "package-contract"
        and item.get("command") == "python3 scripts/check.py"
        and item.get("expect_exit") == 0
        and not isinstance(item.get("expect_exit"), bool)
        for item in static
    ):
        add(
            errors, "evals/evals.json: static must declare the package-contract command"
        )
    cases = payload.get("codex_cases")
    if not isinstance(cases, list) or len(cases) < 3:
        add(errors, "evals/evals.json: codex_cases needs at least three cases")
        return
    ids: list[str] = []
    for index, case in enumerate(cases):
        label = f"evals/evals.json codex_cases[{index}]"
        if not isinstance(case, dict):
            add(errors, f"{label}: expected an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            add(errors, f"{label}: id must be a non-empty string")
        else:
            ids.append(case_id)
        for field in ("prompt", "expected_outcome"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                add(errors, f"{label}: {field} must be a non-empty string")
        forbidden = {"result", "score", "duration", "trace"}.intersection(case)
        if forbidden:
            add(
                errors,
                f"{label}: committed results are not allowed ({sorted(forbidden)!r})",
            )
    if len(set(ids)) != len(ids):
        add(errors, "evals/evals.json: codex case IDs must be unique")
    expected_ids = contract.get("eval_case_ids")
    if isinstance(expected_ids, list) and ids != expected_ids:
        add(errors, "evals/evals.json: codex case IDs must match assets/contract.json")
    lowered = " ".join(ids).lower()
    if (
        "positive" not in lowered
        or "near-miss" not in lowered
        or not any(word in lowered for word in ("safety", "failure", "boundary"))
    ):
        add(
            errors,
            "evals/evals.json: include positive, near-miss, and safety/failure/boundary cases",
        )


def check_containment_and_paths(errors: list[str]) -> None:
    root = ROOT.resolve()
    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink():
            try:
                path.resolve().relative_to(root)
            except (OSError, RuntimeError, ValueError):
                add(errors, f"symlink leaves package: {path.relative_to(ROOT)}")
            continue
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if GLOBAL_RE.search(text):
            add(errors, f"global or host-specific path in {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    contract = check_contract(errors)
    check_skill(errors, contract)
    check_openai(errors)
    check_validator(errors)
    check_evals(errors, contract)
    check_containment_and_paths(errors)
    if errors:
        for error in errors:
            print(f"FAIL {ROOT.name}: {error}", file=sys.stderr)
        return 1
    print(f"PASS {ROOT.name} package contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
