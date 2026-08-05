"""Exception-contract parsing and application."""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from pathlib import Path, PurePosixPath

from .records import (
    ArtifactException,
    Finding,
    NamingException,
    SyntaxRule,
    TestSourceRoot,
)
from .rules import (
    ARTIFACT_EXCEPTION_CLASSES,
    LOW_QUALITY_EXCEPTION_VALUES,
    NAMING_EXCEPTION_RULES,
)


def exception_path_is_overbroad(value: str) -> bool:
    pure = PurePosixPath(value)
    return pure.is_absolute() or ".." in pure.parts or "\x00" in value or value in {"", "."} or pure.as_posix() != value or any(char in value for char in "*?[]\\")


def exception_quality_error(raw: dict[str, str]) -> str | None:
    values = {key: raw[key].strip().lower() for key in ("reason", "owner", "control", "review")}
    if len(values["reason"]) < 12 or len(values["owner"]) < 3 or len(values["control"]) < 8 or len(values["review"]) < 8 or any(value in LOW_QUALITY_EXCEPTION_VALUES for value in values.values()):
        return "must name a specific contract, accountable owner, testable control, and review/removal trigger"
    if re.search(r"\b(convenience|refactor cost)\b", values["reason"]):
        return "reason cannot be convenience or refactor cost"
    authority = re.compile(r"\b(abi|api|compiler|deployment|external|generator|golden|package export|protocol|public|published|runner|schema|toolchain|upstream|wire)\b")
    if not authority.search(values["reason"]):
        return "reason must name the compiler, generator, runner, upstream, or published contract"
    if re.search(r"\b(manual|none|n/a)\b", values["control"]) or not re.search(r"\b(check|checksum|ci|diff|gate|lock|monitor|test|validator|verification)\w*\b", values["control"]):
        return "control must be an automated or independently testable check"
    if re.search(r"\b(never|none|permanent)\b", values["review"]) or not re.search(r"\b(date|expires?|migration|release|remove|sunset|upgrade|version|v\d+)\b", values["review"]):
        return "review must name a date, release, version, upgrade, migration, or removal trigger"
    return None


def load_exceptions(root: Path, path: Path | None) -> tuple[list[NamingException], list[ArtifactException], list[Finding]]:
    if path is None:
        path = root / ".architecture-enforcement.json"
        if not path.exists():
            return [], [], []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [], [Finding("error", "invalid-exception-file", path, f"cannot read exception contract: {exc}")]
    allowed_keys = {"artifact_exemptions", "naming_exceptions", "syntax_rules", "test_source_roots"}
    if not isinstance(payload, dict) or not payload or not set(payload) <= allowed_keys:
        return [], [], [Finding("error", "invalid-exception-file", path, "top-level object may contain only naming_exceptions, artifact_exemptions, syntax_rules, and test_source_roots arrays")]
    naming_records, artifact_records = payload.get("naming_exceptions", []), payload.get("artifact_exemptions", [])
    if not isinstance(naming_records, list) or not isinstance(artifact_records, list):
        return [], [], [Finding("error", "invalid-exception-file", path, "exception collections must be arrays")]
    findings: list[Finding] = []
    valid: list[NamingException] = []
    required = {"rule", "path", "reason", "owner", "control", "review"}
    for index, raw in enumerate(naming_records):
        if not isinstance(raw, dict) or set(raw) != required or any(not isinstance(raw.get(key), str) or not raw[key].strip() for key in required):
            findings.append(Finding("error", "invalid-naming-exception", path, f"exception {index} must contain exactly six nonempty string fields"))
        elif exception_path_is_overbroad(raw["path"]):
            findings.append(Finding("error", "invalid-naming-exception", path, f"exception {index} path must be exact and root-relative"))
        elif raw["rule"] not in NAMING_EXCEPTION_RULES:
            findings.append(Finding("error", "invalid-naming-exception", path, f"exception {index} has unknown naming rule '{raw['rule']}'"))
        elif quality_error := exception_quality_error(raw):
            findings.append(Finding("error", "invalid-naming-exception", path, f"exception {index} {quality_error}"))
        else:
            valid.append(NamingException(**{key: raw[key].strip() for key in required}))
    artifacts: list[ArtifactException] = []
    required = {"class", "path", "reason", "owner", "control", "review"}
    for index, raw in enumerate(artifact_records):
        if not isinstance(raw, dict) or set(raw) != required or any(not isinstance(raw.get(key), str) or not raw[key].strip() for key in required):
            findings.append(Finding("error", "invalid-artifact-exemption", path, f"artifact exemption {index} must contain exactly six nonempty string fields"))
        elif exception_path_is_overbroad(raw["path"]):
            findings.append(Finding("error", "invalid-artifact-exemption", path, f"artifact exemption {index} path must be exact and root-relative"))
        elif raw["class"] not in ARTIFACT_EXCEPTION_CLASSES:
            findings.append(Finding("error", "invalid-artifact-exemption", path, f"artifact exemption {index} has unknown class '{raw['class']}'"))
        elif quality_error := exception_quality_error(raw):
            findings.append(Finding("error", "invalid-artifact-exemption", path, f"artifact exemption {index} {quality_error}"))
        else:
            artifacts.append(ArtifactException(raw["class"].strip(), raw["path"].strip(), raw["reason"].strip(), raw["owner"].strip(), raw["control"].strip(), raw["review"].strip()))
    return valid, artifacts, findings


def load_test_source_roots(root: Path, path: Path | None) -> tuple[list[TestSourceRoot], list[Finding]]:
    """Load exact, reviewed custom test-source roots without accepting globs."""
    if path is None:
        path = root / ".architecture-enforcement.json"
        if not path.exists():
            return [], []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], []
    if not isinstance(payload, dict) or "test_source_roots" not in payload:
        return [], []
    records = payload["test_source_roots"]
    if not isinstance(records, list):
        return [], [Finding("error", "invalid-test-source-root", path, "test_source_roots must be an array")]
    required = {"path", "reason", "owner", "control", "review"}
    roots: list[TestSourceRoot] = []
    findings: list[Finding] = []
    for index, raw in enumerate(records):
        if (
            not isinstance(raw, dict)
            or set(raw) != required
            or any(not isinstance(raw.get(key), str) or not raw[key].strip() for key in required)
        ):
            findings.append(Finding("error", "invalid-test-source-root", path, f"test source root {index} must contain exactly five nonempty string fields"))
        elif exception_path_is_overbroad(raw["path"]):
            findings.append(Finding("error", "invalid-test-source-root", path, f"test source root {index} path must be exact and root-relative"))
        elif quality_error := exception_quality_error(raw):
            findings.append(Finding("error", "invalid-test-source-root", path, f"test source root {index} {quality_error}"))
        else:
            roots.append(TestSourceRoot(**{key: raw[key].strip() for key in required}))
    return roots, findings


def load_syntax_rules(root: Path, path: Path | None) -> tuple[list[SyntaxRule], list[Finding]]:
    """Load fixed-provider syntax rules without accepting command strings."""

    if path is None:
        path = root / ".architecture-enforcement.json"
        if not path.exists():
            return [], []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], []
    if not isinstance(payload, dict):
        return [], []
    records = payload.get("syntax_rules", [])
    if not isinstance(records, list):
        return [], [Finding("error", "invalid-syntax-rule", path, "syntax_rules must be an array")]
    required = {"id", "tool", "language", "pattern", "severity", "message", "mode"}
    allowed = required | {"paths"}
    rules: list[SyntaxRule] = []
    findings: list[Finding] = []
    for index, raw in enumerate(records):
        if not isinstance(raw, dict) or set(raw) - allowed or not required <= set(raw):
            findings.append(Finding("error", "invalid-syntax-rule", path, f"syntax rule {index} must contain exactly the required fields and optional paths"))
            continue
        if any(not isinstance(raw[key], str) or not raw[key].strip() for key in required):
            findings.append(Finding("error", "invalid-syntax-rule", path, f"syntax rule {index} has an empty or non-string required field"))
            continue
        if raw["tool"] not in {"ast-grep"}:
            findings.append(Finding("error", "invalid-syntax-rule", path, f"syntax rule {index} uses unsupported provider '{raw['tool']}'"))
            continue
        if raw["severity"] not in {"error", "warning"} or raw["mode"] != "required":
            findings.append(Finding("error", "invalid-syntax-rule", path, f"syntax rule {index} must use severity error/warning and required mode; advisory and notice rules cannot be accepted"))
            continue
        paths = raw.get("paths", [])
        if not isinstance(paths, list) or any(not isinstance(item, str) or not item or item.startswith("/") or ".." in PurePosixPath(item).parts for item in paths):
            findings.append(Finding("error", "invalid-syntax-rule", path, f"syntax rule {index} paths must be root-relative strings without '..'"))
            continue
        rules.append(SyntaxRule(raw["id"].strip(), raw["tool"].strip(), raw["language"].strip(), raw["pattern"], raw["severity"], raw["message"].strip(), raw["mode"], tuple(paths)))
    return rules, findings
