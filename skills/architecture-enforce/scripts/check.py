"""Package-local static contract check for one portable skill."""
from __future__ import annotations

import json
import re
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
REQUIRED_FILES = [
    "SKILL.md",
    "LICENSE",
    ".skill-validator.json",
    "agents/openai.yaml",
    "references",
    "assets/contract.json",
    "evals/evals.json",
    "scripts/check.py",
]
GLOBAL_PATH = re.compile(
    r"(?<![A-Za-z0-9_])(?:/(?:Users|home|root|tmp)(?:[/\\]|$)|"
    r"(?:~|\$HOME)(?:[/\\]|$)|[A-Za-z]:[/\\](?:Users|home)(?:[/\\]|$))"
)


def safe_path(raw: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        errors.append(f"{label} must be a non-empty relative path")
        return None
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label} leaves package root: {raw!r}")
        return None
    return path


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        errors.append("SKILL.md frontmatter has no closing delimiter")
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not match:
            continue
        value = (match.group(2) or "").strip().strip('"').strip("'")
        fields[match.group(1)] = value
    return fields


def read_json(path: Path, label: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is not valid JSON: {exc}")
        return None


def check_required_files(contract: dict[str, object], errors: list[str]) -> None:
    required = contract.get("required_files")
    if required != REQUIRED_FILES:
        errors.append("contract.required_files must equal the common package list")
        return
    for raw in required:
        relative = safe_path(raw, "contract.required_files entry", errors)
        if relative is None:
            continue
        target = ROOT / relative
        if raw == "references":
            if not target.is_dir():
                errors.append("missing required directory: references")
        elif not target.is_file():
            errors.append(f"missing required file: {raw}")


def check_yaml(errors: list[str], skill_name: str) -> None:
    path = ROOT / "agents" / "openai.yaml"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"agents/openai.yaml cannot be read: {exc}")
        return
    values: dict[str, str] = {}
    for line in lines:
        match = re.match(r"^\s*(display_name|short_description|default_prompt):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    for key in ("display_name", "short_description", "default_prompt"):
        if not values.get(key):
            errors.append(f"agents/openai.yaml requires interface.{key}")
    prompts = re.findall(r"\$[a-z0-9-]+", values.get("default_prompt", ""))
    if prompts != [f"${skill_name}"]:
        errors.append(
            "agents/openai.yaml default_prompt must invoke exactly "
            f"${skill_name} (found {prompts!r})"
        )


def check_evals(contract: dict[str, object], errors: list[str], skill_name: str) -> None:
    path = ROOT / "evals" / "evals.json"
    payload = read_json(path, "evals/evals.json", errors)
    if not isinstance(payload, dict):
        return
    if payload.get("schema_version") != 1:
        errors.append("evals/evals.json schema_version must be 1")
    if payload.get("skill_name") != skill_name:
        errors.append("evals/evals.json skill_name must match package name")
    static = payload.get("static")
    if not isinstance(static, list) or not static:
        errors.append("evals/evals.json requires a non-empty static array")
    else:
        package_checks = [item for item in static if isinstance(item, dict) and item.get("id") == "package-contract"]
        if len(package_checks) != 1:
            errors.append("evals/evals.json requires one package-contract static check")
        for item in static:
            if not isinstance(item, dict) or item.get("command") != "python3 scripts/check.py" or item.get("expect_exit") != 0:
                errors.append("every static check must run python3 scripts/check.py with expect_exit 0")
    cases = payload.get("codex_cases")
    if not isinstance(cases, list) or len(cases) < 3:
        errors.append("evals/evals.json requires at least three codex_cases")
        return
    ids: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"codex_cases[{index}] must be an object")
            continue
        if set(case) != {"id", "prompt", "expected_outcome"}:
            errors.append(f"codex_cases[{index}] must contain only id, prompt, expected_outcome")
        for key in ("id", "prompt", "expected_outcome"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f"codex_cases[{index}] requires a non-empty string {key}")
        if isinstance(case.get("id"), str):
            ids.append(case["id"])
    expected_ids = contract.get("eval_case_ids")
    if ids != expected_ids:
        errors.append("contract.eval_case_ids must match codex_cases IDs in order")
    lower = " ".join(ids).lower()
    if "positive" not in lower or not ("near-miss" in lower or "near_miss" in lower) or not any(word in lower for word in ("safety", "failure", "boundary")):
        errors.append("codex_cases must include positive, near-miss, and safety/failure/boundary IDs")


def check_contract(skill_text: str, errors: list[str], skill_name: str) -> None:
    path = ROOT / "assets" / "contract.json"
    payload = read_json(path, "assets/contract.json", errors)
    if not isinstance(payload, dict):
        return
    if payload.get("schema_version") != 1:
        errors.append("assets/contract.json schema_version must be 1")
    if payload.get("skill_name") != skill_name:
        errors.append("assets/contract.json skill_name must match package name")
    if payload.get("required_headings") != HEADINGS:
        errors.append("contract.required_headings must equal the common heading list")
    check_required_files(payload, errors)
    refs = payload.get("reference_paths")
    if not isinstance(refs, list) or not refs:
        errors.append("contract.reference_paths must be a non-empty array")
    else:
        for raw in refs:
            relative = safe_path(raw, "contract.reference_paths entry", errors)
            if relative is None:
                continue
            if not str(raw).startswith("references/") or not (ROOT / relative).is_file():
                errors.append(f"missing package reference: {raw}")
            if str(raw) not in skill_text:
                errors.append(f"reference not routed by SKILL.md: {raw}")
    ids = payload.get("eval_case_ids")
    if not isinstance(ids, list) or len(ids) < 3 or any(not isinstance(item, str) or not item for item in ids) or len(set(ids)) != len(ids):
        errors.append("contract.eval_case_ids must contain at least three unique IDs")
    check_evals(payload, errors, skill_name)


def check_skill(errors: list[str], skill_name: str) -> str:
    path = ROOT / "SKILL.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"SKILL.md cannot be read: {exc}")
        return ""
    fields = parse_frontmatter(text, errors)
    if fields.get("name") != skill_name:
        errors.append("SKILL.md frontmatter name must match package directory")
    if not fields.get("description") or fields.get("description") == ">":
        errors.append("SKILL.md frontmatter description must be non-empty")
    titles = re.findall(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if len(titles) != 1:
        errors.append("SKILL.md must contain exactly one H1 title")
    headings = set(re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
    missing = [heading for heading in HEADINGS if heading not in headings]
    errors.extend(f"SKILL.md missing heading: ## {heading}" for heading in missing)
    if len(text.splitlines()) > 260:
        errors.append("SKILL.md exceeds 260 lines")
    return text


def check_paths(errors: list[str]) -> None:
    root = ROOT.resolve()
    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink():
            try:
                path.resolve().relative_to(root)
            except ValueError:
                errors.append(f"symlink leaves package root: {path.relative_to(ROOT)}")
            continue
        if not path.is_file() or path.suffix == ".pyc" or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if GLOBAL_PATH.search(line) and not line.lstrip().startswith("http"):
                errors.append(f"global/host path in {path.relative_to(ROOT)}:{line_no}")


def main() -> int:
    errors: list[str] = []
    skill_name = ROOT.name
    skill_text = check_skill(errors, skill_name)
    check_contract(skill_text, errors, skill_name)
    check_yaml(errors, skill_name)
    check_paths(errors)
    if errors:
        print(f"FAIL: {skill_name}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {skill_name} package-contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
