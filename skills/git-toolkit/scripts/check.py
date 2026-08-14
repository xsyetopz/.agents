"""Check one copied skill package using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = [
    "When to use",
    "When NOT to use",
    "Guardrails",
    "Workflow",
    "Quick start",
    "Reference map",
    "Completion",
    "Validation",
    "Related skills",
]
FILES = [
    "SKILL.md",
    "LICENSE",
    ".skill-validator.json",
    "agents/openai.yaml",
    "references",
    "assets/contract.json",
    "evals/evals.json",
    "scripts/check.py",
]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
GLOBAL_MARKERS = (
    "/" + "Users/",
    "/" + "home/",
    "/" + "root/",
    "/" + "tmp/",
    "$" + "HOME/",
    "~" + "/" + ".agents/",
    "~" + "/" + ".codex/",
)
WINDOWS_GLOBAL = re.compile(
    r"[A-Za-z]:[\\/]" + "(?:Users|home|.agents|.codex)" + r"[\\/]"
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_json(path: Path, errors: list[str], label: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(errors, f"{label}: invalid JSON ({exc})")
        return None


def frontmatter(text: str, errors: list[str]) -> tuple[str | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(errors, "SKILL.md: frontmatter must start on line 1")
        return None, None
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(errors, "SKILL.md: frontmatter closing marker is missing")
        return None, None
    name = None
    description_parts: list[str] = []
    in_description = False
    for line in lines[1:end]:
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("'\"")
            in_description = False
        elif line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            in_description = value in {">", ">-", ">+", "|", "|-", "|+"}
            if value and not in_description:
                description_parts.append(value.strip("'\""))
        elif in_description and line.startswith((" ", "\t")):
            description_parts.append(line.strip())
        elif line.strip():
            in_description = False
    description = " ".join(description_parts).strip() or None
    if not name:
        fail(errors, "SKILL.md: frontmatter requires name")
    if not description:
        fail(errors, "SKILL.md: frontmatter requires description")
    if name and name != ROOT.name:
        fail(errors, f"SKILL.md: name {name!r} does not match package {ROOT.name!r}")
    return name, description


def safe_path(relative: str, errors: list[str]) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(errors, f"contract: path leaves package root: {relative}")
        return None
    resolved = (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        fail(errors, f"contract: path leaves package root: {relative}")
        return None
    return resolved


def check_contract(errors: list[str]) -> tuple[dict, list[str]]:
    contract_path = ROOT / "assets" / "contract.json"
    contract = read_json(contract_path, errors, "assets/contract.json")
    if not isinstance(contract, dict):
        return {}, []
    allowed = {
        "schema_version",
        "skill_name",
        "required_headings",
        "required_files",
        "reference_paths",
        "eval_case_ids",
    }
    unknown = sorted(set(contract) - allowed)
    if unknown:
        fail(errors, f"assets/contract.json: unsupported fields: {', '.join(unknown)}")
    if contract.get("schema_version") != 1:
        fail(errors, "assets/contract.json: schema_version must be 1")
    if contract.get("skill_name") != ROOT.name:
        fail(errors, "assets/contract.json: skill_name must match package directory")
    if contract.get("required_headings") != HEADINGS:
        fail(
            errors,
            "assets/contract.json: required_headings must use the common ordered list",
        )
    if contract.get("required_files") != FILES:
        fail(
            errors,
            "assets/contract.json: required_files must use the common ordered list",
        )
    refs = contract.get("reference_paths")
    if not isinstance(refs, list) or not refs:
        fail(errors, "assets/contract.json: reference_paths must be a non-empty array")
        refs = []
    for relative in refs:
        if (
            not isinstance(relative, str)
            or not relative.startswith("references/")
            or not relative.endswith(".md")
        ):
            fail(errors, f"assets/contract.json: invalid reference path: {relative!r}")
            continue
        target = safe_path(relative, errors)
        if target is not None and not target.is_file():
            fail(errors, f"assets/contract.json: missing reference: {relative}")
    ids = contract.get("eval_case_ids")
    if (
        not isinstance(ids, list)
        or len(ids) < 3
        or any(not isinstance(item, str) or not item.strip() for item in ids)
    ):
        fail(
            errors,
            "assets/contract.json: eval_case_ids needs at least three non-empty strings",
        )
        ids = []
    if len(set(ids)) != len(ids):
        fail(errors, "assets/contract.json: eval_case_ids must be unique")
    return contract, refs


def check_files(contract: dict, errors: list[str]) -> None:
    for relative in contract.get("required_files", []):
        target = safe_path(relative, errors)
        if target is None:
            continue
        expected_dir = relative in {"references"}
        if expected_dir and not target.is_dir():
            fail(errors, f"required directory is missing: {relative}")
        elif not expected_dir and not target.is_file():
            fail(errors, f"required file is missing: {relative}")


def check_skill(text: str, contract: dict, refs: list[str], errors: list[str]) -> None:
    _name, _description = frontmatter(text, errors)
    headings = {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    }
    for heading in contract.get("required_headings", []):
        if heading not in headings:
            fail(errors, f"SKILL.md: missing required heading: ## {heading}")
    if not re.search(r"^#\s+\S+", text, re.MULTILINE):
        fail(errors, "SKILL.md: a title heading is required")
    for relative in refs:
        if f"]({relative})" not in text and f"](./{relative})" not in text:
            fail(
                errors,
                f"SKILL.md: reference is not routed in Reference map: {relative}",
            )
    for raw in LINK.findall(text):
        target = raw.split("#", 1)[0].split("?", 1)[0].strip()
        if not target or target.startswith(
            ("http://", "https://", "mailto:", "#", "//")
        ):
            continue
        path = safe_path(target, errors)
        if path is not None and not path.exists():
            fail(errors, f"SKILL.md: broken local link: {target}")


def check_evals(contract: dict, errors: list[str]) -> None:
    evals = read_json(ROOT / "evals" / "evals.json", errors, "evals/evals.json")
    if not isinstance(evals, dict):
        return
    if evals.get("schema_version") != 1 or evals.get("skill_name") != ROOT.name:
        fail(
            errors,
            "evals/evals.json: schema_version must be 1 and skill_name must match package",
        )
    static = evals.get("static")
    if not isinstance(static, list) or not any(
        isinstance(item, dict)
        and item.get("id") == "package-contract"
        and item.get("command") == "python3 scripts/check.py"
        and item.get("expect_exit") == 0
        for item in static
    ):
        fail(errors, "evals/evals.json: static package-contract command is required")
    cases = evals.get("codex_cases")
    ids = contract.get("eval_case_ids", [])
    if not isinstance(cases, list) or len(cases) < 3:
        fail(errors, "evals/evals.json: codex_cases needs at least three cases")
        return
    seen: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(errors, f"evals/evals.json: codex_cases[{index}] must be an object")
            continue
        if set(case) != {"id", "prompt", "expected_outcome"}:
            fail(errors, f"evals/evals.json: codex_cases[{index}] has the wrong fields")
            continue
        if any(
            not isinstance(case[field], str) or not case[field].strip()
            for field in case
        ):
            fail(
                errors,
                f"evals/evals.json: codex_cases[{index}] fields must be non-empty strings",
            )
        seen.append(case.get("id", ""))
    if seen != ids:
        fail(
            errors,
            "evals/evals.json: codex case IDs must match contract eval_case_ids in order",
        )
    lowered = {item.lower() for item in seen}
    if not any("positive" in item for item in lowered):
        fail(errors, "evals/evals.json: include a positive case")
    if not any("near-miss" in item or "near_miss" in item for item in lowered):
        fail(errors, "evals/evals.json: include a near-miss case")
    if not any(
        any(word in item for word in ("safety", "failure", "boundary"))
        for item in lowered
    ):
        fail(errors, "evals/evals.json: include a safety/failure/boundary case")


def check_global_paths(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if any(
                marker in line for marker in GLOBAL_MARKERS
            ) or WINDOWS_GLOBAL.search(line):
                fail(errors, f"global/host path in {path.relative_to(ROOT)}:{line_no}")


def main() -> int:
    errors: list[str] = []
    contract, refs = check_contract(errors)
    check_files(contract, errors)
    skill_path = ROOT / "SKILL.md"
    try:
        skill_text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(errors, f"SKILL.md: unable to read ({exc})")
        skill_text = ""
    check_skill(skill_text, contract, refs, errors)
    check_evals(contract, errors)
    check_global_paths(errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {ROOT.name} package contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
