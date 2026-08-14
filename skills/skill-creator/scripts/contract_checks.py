"""Specification and package-contract checks for the skill validator."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from reference_checks import HEADING_RE, strip_fenced_blocks

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_MD_LINE_WARN = 500
SKILL_MD_LINE_ERROR = 800
COMMON_CONTRACT_HEADINGS = [
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
COMMON_CONTRACT_FILES = [
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
STATIC_EVAL_KEYS = {"id", "command", "expect_exit"}
CODEX_CASE_KEYS = {"id", "prompt", "expected_outcome"}


def load_config(root: Path) -> dict[str, Any]:
    config_path = root / ".skill-validator.json"
    if not config_path.is_file():
        return {}
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid .skill-validator.json: {exc}") from exc
    if not isinstance(config, dict):
        raise TypeError(".skill-validator.json must contain a JSON object.")
    return config


# --- Spec compliance checks ---


def check_frontmatter_spec(fm: dict, root: Path, errors: list[str]) -> None:
    """Validate frontmatter against the Agent Skills specification."""
    name = fm.get("name", "")
    description = fm.get("description", "")

    if not isinstance(name, str) or not name.strip():
        errors.append("Frontmatter requires non-empty 'name'.")
    else:
        if len(name) > 64:
            errors.append(f"'name' exceeds 64 characters (got {len(name)}).")
        if not NAME_RE.fullmatch(name):
            errors.append(
                "'name' must be lowercase letters/digits separated by single hyphens, "
                "no leading/trailing hyphens, no consecutive hyphens."
            )
        if name.startswith("-") or name.endswith("-"):
            errors.append("'name' must not start or end with a hyphen.")
        if "--" in name:
            errors.append("'name' must not contain consecutive hyphens.")

    if isinstance(name, str) and root.name != name:
        errors.append(f"Folder name {root.name!r} must match skill name {name!r}.")

    if not isinstance(description, str) or not description.strip():
        errors.append("Frontmatter requires non-empty 'description'.")
    elif len(description) > 1024:
        errors.append(
            f"'description' exceeds 1024 characters (got {len(description)})."
        )

    for field in ("license", "allowed-tools"):
        if field in fm and not isinstance(fm[field], str):
            errors.append(f"'{field}' must be a string.")

    if "compatibility" in fm:
        compatibility = fm["compatibility"]
        if not isinstance(compatibility, str):
            errors.append("'compatibility' must be a string.")
        elif not 1 <= len(compatibility) <= 500:
            errors.append(
                f"'compatibility' must be 1-500 characters (got {len(compatibility)})."
            )

    if "metadata" in fm:
        metadata = fm["metadata"]
        if not isinstance(metadata, dict):
            errors.append(
                "'metadata' must be a mapping of string keys to string values."
            )
        else:
            invalid_keys = getattr(metadata, "invalid_keys", [])
            for key in [*invalid_keys, *metadata.keys()]:
                if not isinstance(key, str):
                    errors.append(f"'metadata' key {key!r} must be a string.")
            for key, value in metadata.items():
                if not isinstance(value, str):
                    errors.append(f"'metadata' value for key {key!r} must be a string.")


def check_file_size(root: Path, errors: list[str], warnings: list[str]) -> None:
    """Enforce SKILL.md size limits per progressive disclosure guidelines."""
    skill_file = root / "SKILL.md"
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"Unable to read SKILL.md for size checks: {exc}")
        return
    line_count = len(text.splitlines())

    if line_count > SKILL_MD_LINE_ERROR:
        errors.append(
            f"SKILL.md is {line_count} lines — hard limit is {SKILL_MD_LINE_ERROR}. "
            "Split content into references/ files."
        )
    elif line_count > SKILL_MD_LINE_WARN:
        warnings.append(
            f"SKILL.md has {line_count} lines; spec recommends ≤ {SKILL_MD_LINE_WARN}. "
            "Move detailed material to references/."
        )

    rough_tokens = len(re.findall(r"\w+|[^\w\s]", text))
    if rough_tokens > 7000:
        warnings.append(
            f"SKILL.md rough token count is {rough_tokens}; "
            "progressive disclosure may be weakened."
        )


def check_progressive_disclosure(root: Path, errors: list[str]) -> None:
    """Reject monolithic SKILL.md that violates progressive disclosure."""
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        return
    try:
        line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"Unable to read SKILL.md for disclosure checks: {exc}")
        return
    if line_count > SKILL_MD_LINE_WARN and not (root / "references").is_dir():
        errors.append(
            f"SKILL.md is {line_count} lines with no references/ directory. "
            "Split detailed content into references/ per progressive disclosure spec."
        )


def _config_entries(config: dict, key: str, errors: list[str]) -> list[str]:
    """Return validated string entries from the package-local contract."""
    if key not in config:
        return []
    entries = config[key]
    if not isinstance(entries, list):
        errors.append(f".skill-validator.json '{key}' must be an array of strings.")
        return []
    valid: list[str] = []
    for entry in entries:
        if not isinstance(entry, str) or not entry.strip():
            errors.append(
                f".skill-validator.json '{key}' entries must be non-empty strings."
            )
            continue
        valid.append(entry)
    return valid


def check_required_headings(text: str, config: dict, errors: list[str]) -> None:
    headings = {
        line.strip()
        for line in strip_fenced_blocks(text).splitlines()
        if HEADING_RE.match(line.strip())
    }
    for heading in _config_entries(config, "required_headings", errors):
        if heading not in headings:
            errors.append(f"Missing required heading: {heading}")


def check_required_files(root: Path, config: dict, errors: list[str]) -> None:
    for relative in _config_entries(config, "required_files", errors):
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(
                f".skill-validator.json required file leaves skill root: {relative}"
            )
            continue
        try:
            target = (root / candidate).resolve()
        except (OSError, RuntimeError) as exc:
            errors.append(f"Unable to resolve required file {relative}: {exc}")
            continue
        try:
            target.relative_to(root.resolve())
        except ValueError:
            errors.append(
                f".skill-validator.json required file leaves skill root: {relative}"
            )
            continue
        if not target.is_file():
            errors.append(f"Missing required file: {relative}")


def _read_json(path: Path, label: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid {label}: {exc}")
        return None


def _safe_contract_path(
    root: Path, raw: object, label: str, errors: list[str]
) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        errors.append(f"{label} must be a non-empty package-relative path.")
        return None
    relative = Path(raw)
    if relative.is_absolute() or ".." in relative.parts:
        errors.append(f"{label} leaves skill root: {raw}")
        return None
    target = (root / relative).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label} leaves skill root: {raw}")
        return None
    return target


def _reference_is_routed(reference: str, route_text: str, index_text: str) -> bool:
    """Accept a direct path or a basename route from references/index.md."""
    if reference in route_text:
        return True
    name = Path(reference).name
    # Index links are relative to references/, so the contract prefix is absent.
    return bool(re.search(rf"\]\(\s*(?:\./)?{re.escape(name)}(?:[#?)]|$)", index_text))


def check_assets_contract(
    root: Path, config: dict, skill_text: str, errors: list[str]
) -> dict[str, Any] | None:
    """Validate ``assets/contract.json`` when the package config requires it."""
    configured = config.get("required_files")
    if not isinstance(configured, list) or "assets/contract.json" not in configured:
        return None
    path = root / "assets" / "contract.json"
    payload = _read_json(path, "assets/contract.json", errors)
    if not isinstance(payload, dict):
        errors.append("assets/contract.json must contain a JSON object.")
        return None
    if set(payload) != CONTRACT_KEYS:
        errors.append(
            "assets/contract.json must use exactly schema_version, skill_name, "
            "required_headings, required_files, reference_paths, and eval_case_ids."
        )
    if (
        type(payload.get("schema_version")) is not int
        or payload.get("schema_version") != 1
    ):
        errors.append("assets/contract.json schema_version must be 1.")
    if payload.get("skill_name") != root.name:
        errors.append(
            "assets/contract.json skill_name must match the package directory."
        )

    configured_headings = [
        heading.removeprefix("## ")
        for heading in _config_entries(config, "required_headings", errors)
        if heading.startswith("## ")
    ]
    if payload.get("required_headings") != COMMON_CONTRACT_HEADINGS:
        errors.append(
            "assets/contract.json required_headings must use the common heading order."
        )
    if configured_headings and configured_headings != COMMON_CONTRACT_HEADINGS:
        errors.append(
            ".skill-validator.json required_headings must contain the common heading order."
        )

    if payload.get("required_files") != COMMON_CONTRACT_FILES:
        errors.append(
            "assets/contract.json required_files must use the common package contract."
        )

    references = payload.get("reference_paths")
    if not isinstance(references, list) or not references:
        errors.append("assets/contract.json reference_paths must be a non-empty array.")
        references = []
    valid_references = [
        reference for reference in references if isinstance(reference, str)
    ]
    # The root index is the canonical second hop for larger reference sets.
    # Keep direct SKILL.md routes valid for small copied fixtures.
    route_text = skill_text
    index_text = ""
    index_path = root / "references" / "index.md"
    if index_path.is_file():
        try:
            index_text = index_path.read_text(encoding="utf-8")
            route_text += "\n" + index_text
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"Unable to read references/index.md: {exc}")
    if (
        len(valid_references) != len(references)
        or len(set(valid_references)) != len(valid_references)
        or any(
            not reference.startswith("references/") for reference in valid_references
        )
    ):
        errors.append(
            "assets/contract.json reference_paths must be unique package-relative paths."
        )
    for reference in references:
        target = _safe_contract_path(root, reference, "Contract reference", errors)
        if target is not None and not target.is_file():
            errors.append(f"Missing contract reference: {reference}")
        if isinstance(reference, str) and not _reference_is_routed(
            reference, route_text, index_text
        ):
            errors.append(
                f"Reference map/index does not link contract reference: {reference}"
            )

    case_ids = payload.get("eval_case_ids")
    if (
        not isinstance(case_ids, list)
        or not case_ids
        or any(
            not isinstance(case_id, str) or not case_id.strip() for case_id in case_ids
        )
    ):
        errors.append("assets/contract.json eval_case_ids must be non-empty strings.")
        case_ids = []
    valid_case_ids = [case_id for case_id in case_ids if isinstance(case_id, str)]
    if len(valid_case_ids) != len(case_ids) or len(set(valid_case_ids)) != len(
        valid_case_ids
    ):
        errors.append("assets/contract.json eval_case_ids must be unique.")
    return payload


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_required_evals(
    root: Path,
    config: dict,
    errors: list[str],
    contract: dict[str, Any] | None = None,
) -> None:
    """Validate the canonical package eval manifest without executing prompts."""
    configured = config.get("required_files")
    if not isinstance(configured, list) or "evals/evals.json" not in configured:
        return
    evals_path = root / "evals" / "evals.json"
    payload = _read_json(evals_path, "required evals/evals.json", errors)
    if not isinstance(payload, dict):
        errors.append("evals/evals.json must contain a JSON object.")
        return
    if set(payload) != EVAL_KEYS:
        errors.append(
            "evals/evals.json must use exactly schema_version, skill_name, static, "
            "and codex_cases."
        )
    if (
        type(payload.get("schema_version")) is not int
        or payload.get("schema_version") != 1
    ):
        errors.append("evals/evals.json schema_version must be 1.")
    skill_name = payload.get("skill_name")
    if not _non_empty_string(skill_name):
        errors.append("evals/evals.json requires a non-empty string 'skill_name'.")
    elif skill_name != root.name:
        errors.append("evals/evals.json skill_name must match the package directory.")

    static = payload.get("static")
    if not isinstance(static, list) or not static:
        errors.append("evals/evals.json requires a non-empty 'static' array.")
    else:
        static_ids: list[str] = []
        for index, item in enumerate(static):
            prefix = f"evals/evals.json static[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object.")
                continue
            if set(item) != STATIC_EVAL_KEYS:
                errors.append(
                    f"{prefix} must contain only id, command, and expect_exit."
                )
            if not _non_empty_string(item.get("id")):
                errors.append(f"{prefix} requires a non-empty string 'id'.")
            else:
                static_ids.append(item["id"])
            if not _non_empty_string(item.get("command")):
                errors.append(f"{prefix} requires a non-empty string 'command'.")
            expect_exit = item.get("expect_exit")
            if not isinstance(expect_exit, int) or isinstance(expect_exit, bool):
                errors.append(f"{prefix} requires an integer 'expect_exit'.")
            if item.get("id") == "package-contract" and (
                item.get("command") != "python3 scripts/check.py" or expect_exit != 0
            ):
                errors.append(
                    "package-contract static eval must invoke python3 scripts/check.py "
                    "and expect 0."
                )
        if static_ids.count("package-contract") != 1:
            errors.append(
                "evals/evals.json requires one package-contract static check."
            )

    cases = payload.get("codex_cases")
    if not isinstance(cases, list) or len(cases) < 3:
        errors.append("evals/evals.json requires at least three 'codex_cases'.")
        return
    ids: list[str] = []
    for index, case in enumerate(cases):
        prefix = f"evals/evals.json codex_cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        if set(case) != CODEX_CASE_KEYS:
            errors.append(
                f"{prefix} must contain only id, prompt, and expected_outcome."
            )
        for field in ("id", "prompt", "expected_outcome"):
            if not _non_empty_string(case.get(field)):
                errors.append(f"{prefix} requires a non-empty string '{field}'.")
        if _non_empty_string(case.get("id")):
            ids.append(case["id"])
    if len(set(ids)) != len(ids):
        errors.append("evals/evals.json codex case ids must be unique.")
    if not any(item.startswith("positive-") for item in ids):
        errors.append("evals/evals.json requires a positive codex case.")
    if not any(item.startswith("near-miss-") for item in ids):
        errors.append("evals/evals.json requires a near-miss codex case.")
    if not any(item.startswith(("safety-", "failure-")) for item in ids):
        errors.append("evals/evals.json requires a safety or failure codex case.")
    if contract is not None and ids != contract.get("eval_case_ids"):
        errors.append(
            "assets/contract.json eval_case_ids must match codex case IDs in order."
        )


__all__ = [
    "COMMON_CONTRACT_FILES",
    "COMMON_CONTRACT_HEADINGS",
    "NAME_RE",
    "check_assets_contract",
    "check_file_size",
    "check_frontmatter_spec",
    "check_progressive_disclosure",
    "check_required_evals",
    "check_required_files",
    "check_required_headings",
    "load_config",
]
