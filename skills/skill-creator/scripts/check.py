"""Check the copied skill-creator package without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

EXPECTED_HEADINGS = [
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
CONTRACT_KEYS = {
    "schema_version",
    "skill_name",
    "required_headings",
    "required_files",
    "reference_paths",
    "eval_case_ids",
}
EVAL_KEYS = {"schema_version", "skill_name", "static", "codex_cases"}
CASE_KEYS = {"id", "prompt", "expected_outcome"}
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*([^\s)]+)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FRONT_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")

# Build host-specific path fragments instead of embedding one in this checker.
_HOST_ROOTS = "(?:" + "Users|home|root" + ")"
_TMP_ROOT = "(?:private/)?" + "tmp"
GLOBAL_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:/" + _HOST_ROOTS + r"(?:[/\\][^\s`'\"<>)]*)+"
    r"|/" + _TMP_ROOT + r"(?:[/\\][^\s`'\"<>)]*)+"
    r"|(?:~|\$" + "HOME" + r")(?:[/\\][^\s`'\"<>)]*)+"
    r"|[A-Za-z]:[/\\](?:Users|home|\.agents|\.codex)[/\\][^\s`'\"<>)]*)"
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_json(path: Path, errors: list[str], label: str) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(errors, f"{label}: invalid JSON ({exc})")
        return None


def scalar(raw: str) -> str | None:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return value if isinstance(value, str) else None
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    return raw or None


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(errors, "SKILL.md must begin with YAML frontmatter.")
        return {}
    try:
        end = next(
            index for index in range(1, len(lines)) if lines[index].strip() == "---"
        )
    except StopIteration:
        fail(errors, "SKILL.md frontmatter is not closed.")
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FRONT_KEY_RE.match(line)
        if not match:
            fail(errors, f"SKILL.md frontmatter line is not a scalar mapping: {line!r}")
            continue
        value = scalar(match.group(2))
        if value is None:
            fail(errors, f"SKILL.md frontmatter value is invalid: {line!r}")
            continue
        fields[match.group(1)] = value
    return fields


def markdown_headings(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    fence: str | None = None
    for line in text.splitlines():
        fence_match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            if fence_match and fence_match.group(1)[0] == fence:
                fence = None
            continue
        if fence_match:
            fence = fence_match.group(1)[0]
            continue
        match = HEADING_RE.match(line)
        if match:
            result.append((len(match.group(1)), match.group(2).strip()))
    return result


def safe_relative(root: Path, raw: str, errors: list[str], label: str) -> Path | None:
    target = Path(unquote(raw.split("#", 1)[0].split("?", 1)[0]))
    if target.is_absolute() or ".." in target.parts:
        fail(errors, f"{label} leaves package root: {raw}")
        return None
    candidate = (root / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        fail(errors, f"{label} leaves package root: {raw}")
        return None
    return candidate


def check_contract(
    root: Path, contract: object, errors: list[str]
) -> tuple[list[str], list[str]]:
    if not isinstance(contract, dict):
        fail(errors, "assets/contract.json must contain an object.")
        return [], []
    if set(contract) != CONTRACT_KEYS:
        fail(errors, "assets/contract.json has unexpected or missing schema keys.")
    if contract.get("schema_version") != 1:
        fail(errors, "assets/contract.json schema_version must be 1.")
    if contract.get("skill_name") != root.name:
        fail(
            errors, "assets/contract.json skill_name must match the package directory."
        )
    headings = contract.get("required_headings")
    if headings != EXPECTED_HEADINGS:
        fail(
            errors, "assets/contract.json required_headings must use the common order."
        )
    files = contract.get("required_files")
    if files != EXPECTED_FILES:
        fail(errors, "assets/contract.json required_files must use the common order.")
    references = contract.get("reference_paths")
    if not isinstance(references, list) or not references:
        fail(errors, "assets/contract.json reference_paths must be a non-empty array.")
        references = []
    if len(set(references)) != len(references) or any(
        not isinstance(path, str) or not path.startswith("references/")
        for path in references
    ):
        fail(
            errors,
            "assets/contract.json reference_paths must be unique package-relative paths.",
        )
    for path in references:
        if isinstance(path, str):
            target = safe_relative(root, path, errors, "Contract reference")
            if target is not None and not target.is_file():
                fail(errors, f"Missing contract reference: {path}")
    case_ids = contract.get("eval_case_ids")
    if (
        not isinstance(case_ids, list)
        or not case_ids
        or any(
            not isinstance(case_id, str) or not case_id.strip() for case_id in case_ids
        )
    ):
        fail(errors, "assets/contract.json eval_case_ids must be non-empty strings.")
        case_ids = []
    if len(set(case_ids)) != len(case_ids):
        fail(errors, "assets/contract.json eval_case_ids must be unique.")
    return list(references), list(case_ids)


def check_files(root: Path, files: list[str], errors: list[str]) -> None:
    for relative in files:
        target = safe_relative(root, relative, errors, "Contract file")
        if target is None:
            continue
        expected_dir = relative == "references"
        if expected_dir and not target.is_dir():
            fail(errors, f"Missing required directory: {relative}")
        elif not expected_dir and not target.is_file():
            fail(errors, f"Missing required file: {relative}")


def check_skill(
    root: Path, text: str, frontmatter: dict[str, str], errors: list[str]
) -> None:
    if frontmatter.get("name") != root.name:
        fail(errors, "SKILL.md name must match the package directory.")
    description = frontmatter.get("description", "")
    if not description or len(description) > 1024:
        fail(
            errors,
            "SKILL.md description must be a non-empty string of at most 1024 characters.",
        )
    headings = markdown_headings(text)
    if not headings or headings[0] != (1, "Skill Creator"):
        fail(errors, "SKILL.md must start with '# Skill Creator'.")
    found = {title for level, title in headings if level == 2}
    for title in EXPECTED_HEADINGS:
        if title not in found:
            fail(errors, f"SKILL.md is missing required heading: ## {title}")


def check_links(
    root: Path, text: str, references: list[str], errors: list[str]
) -> None:
    """Check the entrypoint and root reference index as one route graph."""
    mapped: set[str] = set()
    sources = [(root / "SKILL.md", text)]
    index = root / "references" / "index.md"
    if index.is_file():
        try:
            sources.append((index, index.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError) as exc:
            fail(errors, f"references/index.md cannot be read: {exc}")
    else:
        fail(errors, "Missing root reference router: references/index.md")

    for source, source_text in sources:
        for raw in LINK_RE.findall(source_text):
            target = raw.strip().rstrip(".,;:!?)]}")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not relative:
                continue
            candidate = (source.parent / relative).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                fail(errors, f"Markdown link leaves package root: {target}")
                continue
            if not candidate.exists():
                fail(errors, f"Broken Markdown link: {target}")
            try:
                mapped.add(candidate.relative_to(root).as_posix())
            except ValueError:
                continue

    missing = sorted(set(references) - mapped)
    if missing:
        fail(
            errors,
            "Reference map/index does not link every contract reference: "
            + ", ".join(missing),
        )


def check_metadata(root: Path, errors: list[str]) -> None:
    path = root / "agents" / "openai.yaml"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(errors, f"agents/openai.yaml cannot be read: {exc}")
        return
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(
            r"^\s{2}(display_name|short_description|default_prompt):\s*(.*)$", line
        )
        if match:
            value = scalar(match.group(2))
            if value is not None:
                fields[match.group(1)] = value
    for name in ("display_name", "short_description", "default_prompt"):
        if not fields.get(name):
            fail(errors, f"agents/openai.yaml is missing interface.{name}.")
    if not 25 <= len(fields.get("short_description", "")) <= 64:
        fail(errors, "agents/openai.yaml short_description must be 25-64 characters.")
    prompt = fields.get("default_prompt", "")
    token = "$" + root.name
    if prompt.count(token) != 1:
        fail(errors, f"agents/openai.yaml default_prompt must invoke exactly {token}.")


def check_evals(
    root: Path, payload: object, case_ids: list[str], errors: list[str]
) -> None:
    if not isinstance(payload, dict) or set(payload) != EVAL_KEYS:
        fail(
            errors,
            "evals/evals.json must use exactly schema_version, skill_name, static, codex_cases.",
        )
        return
    if payload.get("schema_version") != 1 or payload.get("skill_name") != root.name:
        fail(
            errors,
            "evals/evals.json schema_version/skill_name do not match the package.",
        )
    static = payload.get("static")
    if not isinstance(static, list) or not static:
        fail(errors, "evals/evals.json static must be a non-empty array.")
    else:
        for item in static:
            if not isinstance(item, dict) or set(item) != {
                "id",
                "command",
                "expect_exit",
            }:
                fail(errors, "Each static eval must have id, command, and expect_exit.")
            elif item.get("id") == "package-contract" and (
                item.get("command") != "python3 scripts/check.py"
                or item.get("expect_exit") != 0
            ):
                fail(
                    errors,
                    "package-contract static eval must invoke python3 scripts/check.py and expect 0.",
                )
    cases = payload.get("codex_cases")
    if not isinstance(cases, list) or len(cases) < 3:
        fail(errors, "evals/evals.json requires at least three codex_cases.")
        return
    ids: list[str] = []
    for case in cases:
        if not isinstance(case, dict) or set(case) != CASE_KEYS:
            fail(
                errors,
                "Each codex case must have only id, prompt, and expected_outcome.",
            )
            continue
        if any(
            not isinstance(case[field], str) or not case[field].strip()
            for field in CASE_KEYS
        ):
            fail(
                errors,
                "Each codex case id, prompt, and expected_outcome must be non-empty strings.",
            )
        ids.append(case.get("id", ""))
    if ids != case_ids:
        fail(errors, "Contract eval_case_ids must match eval case order exactly.")
    if not any(item.startswith("positive-") for item in ids):
        fail(errors, "Evals require a positive case.")
    if not any(item.startswith("near-miss-") for item in ids):
        fail(errors, "Evals require a near-miss case.")
    if not any(item.startswith(("safety-", "failure-")) for item in ids):
        fail(errors, "Evals require a safety or failure case.")


def check_paths_and_text(root: Path, errors: list[str]) -> None:
    resolved_root = root.resolve()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            try:
                path.resolve().relative_to(resolved_root)
            except (OSError, RuntimeError, ValueError):
                fail(errors, f"Symlink leaves package root: {path.relative_to(root)}")
            continue
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(content.splitlines(), 1):
            if GLOBAL_PATH_RE.search(line):
                fail(
                    errors,
                    f"Global/host-specific path in {path.relative_to(root)}:{line_no}",
                )
    nested = [
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
        and path.name.casefold() == "skill.md"
        and path.relative_to(root).parts != ("SKILL.md",)
    ]
    if nested:
        fail(
            errors,
            "Nested duplicate SKILL.md entrypoint: " + ", ".join(map(str, nested)),
        )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    try:
        text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(errors, f"SKILL.md cannot be read: {exc}")
        text = ""
    frontmatter = parse_frontmatter(text, errors)
    check_skill(root, text, frontmatter, errors)
    contract = read_json(
        root / "assets" / "contract.json", errors, "assets/contract.json"
    )
    references, case_ids = check_contract(root, contract, errors)
    check_files(root, EXPECTED_FILES, errors)
    check_links(root, text, references, errors)
    check_metadata(root, errors)
    evals = read_json(root / "evals" / "evals.json", errors, "evals/evals.json")
    check_evals(root, evals, case_ids, errors)
    check_paths_and_text(root, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(
        f"PASS: {root} (package contract, metadata, references, evals, and path safety)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
