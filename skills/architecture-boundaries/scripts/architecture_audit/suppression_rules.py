#!/usr/bin/env python3
"""Rules and parsing helpers for lint/check suppression detection."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .records import Finding

_DOCUMENTATION_SUFFIXES = {".adoc", ".md", ".rst", ".txt"}
_HASH_COMMENT_SUFFIXES = {
    ".bash",
    ".cfg",
    ".conf",
    ".fish",
    ".ini",
    ".jl",
    ".nim",
    ".pl",
    ".pm",
    ".py",
    ".pyi",
    ".pyw",
    ".r",
    ".rake",
    ".rb",
    ".sh",
    ".t",
    ".toml",
    ".yaml",
    ".yml",
    ".zsh",
}
_DASH_COMMENT_SUFFIXES = {".hs", ".lhs", ".lua"}
_PERCENT_COMMENT_SUFFIXES = {".erl", ".hrl"}
_SEMICOLON_COMMENT_SUFFIXES = {".clj", ".cljs", ".cljc"}
_COMMENT_DIRECTIVES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "eslint",
        re.compile(
            r"\beslint-disable(?:-(?:next-)?line)?(?=$|[\s:*#/])", re.IGNORECASE
        ),
    ),
    (
        "stylelint",
        re.compile(r"\bstylelint-disable(?:-(?:next-)?line)?\b", re.IGNORECASE),
    ),
    ("biome", re.compile(r"\bbiome-ignore\b", re.IGNORECASE)),
    ("deno", re.compile(r"\bdeno-lint-ignore\b", re.IGNORECASE)),
    ("typescript", re.compile(r"@ts-(?:ignore|nocheck|expect-error)\b", re.IGNORECASE)),
    ("noqa", re.compile(r"\bnoqa\b", re.IGNORECASE)),
    ("type-ignore", re.compile(r"\btype:\s*ignore\b", re.IGNORECASE)),
    ("pylint", re.compile(r"\bpylint\s*:\s*disable\b", re.IGNORECASE)),
    ("rubocop", re.compile(r"\brubocop(?:\s+|\s*:\s*)disable\b", re.IGNORECASE)),
    ("swiftlint", re.compile(r"\bswiftlint(?:\s+|\s*:\s*)disable\b", re.IGNORECASE)),
    ("ktlint", re.compile(r"\bktlint(?:\s+|\s*[-:]\s*)disable\b", re.IGNORECASE)),
    (
        "golangci-lint",
        re.compile(r"\bgolangci-lint(?:\s+|\s*:\s*)disable\b", re.IGNORECASE),
    ),
    ("nolint", re.compile(r"\bnolint(?:nextline|begin|end)?(?:\b|:)", re.IGNORECASE)),
    ("shellcheck", re.compile(r"\bshellcheck\s+disable\b", re.IGNORECASE)),
    ("dart", re.compile(r"\bignore_for_file\s*:", re.IGNORECASE)),
    ("pyright", re.compile(r"\bpyright\s*:\s*ignore\b", re.IGNORECASE)),
    ("go-lint", re.compile(r"\blint\s*:\s*ignore\b", re.IGNORECASE)),
    ("phpstan", re.compile(r"@phpstan-ignore(?:-next-line)?\b", re.IGNORECASE)),
)
_RUST_ALLOW = re.compile(r"^\s*#!?\s*\[[^\]]*\ballow\s*\(", re.IGNORECASE)
_CODE_SUPPRESSIONS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "pragma-warning",
        re.compile(r"^\s*#\s*pragma\s+warning\s+disable\b", re.IGNORECASE),
    ),
    (
        "pragma-diagnostic",
        re.compile(r"^\s*#\s*pragma\s+\w+\s+diagnostic\s+ignored\b", re.IGNORECASE),
    ),
    (
        "suppress-annotation",
        re.compile(r"^\s*@Suppress(?:Warnings)?\s*\(", re.IGNORECASE),
    ),
    ("dotnet-suppress-message", re.compile(r"\bSuppressMessage\s*\(", re.IGNORECASE)),
    ("scala-nowarn", re.compile(r"^\s*@nowarn\b", re.IGNORECASE)),
)
_CHECK_BYPASS = re.compile(
    r"(?ix)(?:"
    r"\b(?:eslint|biome|tsc|pyright|mypy|ruff|pylint|flake8|pytest|jest|vitest|rubocop|"
    r"swiftlint|ktlint|golangci-lint|cargo\s+(?:fmt|clippy|check|test)|go\s+(?:vet|test)|"
    r"npm\s+(?:run\s+)?(?:lint|check|test)|pnpm\s+(?:run\s+)?(?:lint|check|test)|"
    r"yarn\s+(?:run\s+)?(?:lint|check|test)|bun\s+(?:run\s+)?(?:lint|check|test))\b"
    r"|(?:^|[;&|]\s*|(?<![\w-])(?:run|command|script)\s*:\s*)(?:[./\w-]+/)?[\w.-]*(?:lint|check|test|verify|typecheck|fmt)[\w.-]*(?:\s|$)"
    r")[^|\n]*\|\|\s*(?:true\b|:(?=\s|$|[\"']))"
)
_SHELL_COMMENT = re.compile(r"(?<!\w)#")
_CI_BYPASS = re.compile(
    r"^\s*(?:continue-on-error|allow_failure)\s*:\s*(?:true|yes|1)\b", re.IGNORECASE
)
_CI_CONTEXT = re.compile(
    r"(?<![A-Za-z0-9])(?:lint(?:ing)?|checks?|tests?|verify|verification|typecheck(?:ing)?|format(?:ting)?|fmt|clippy|vet)(?![A-Za-z0-9])",
    re.IGNORECASE,
)
_DISABLED_RULE = re.compile(
    r"(?ix)(?:"
    r"[\"']?[\w/@.*:-]+[\"']?\s*:\s*[\"']?(?:off|0|false)[\"']?"
    r"|(?:severity|level)\s*[:=]\s*[\"']?(?:off|0|false)[\"']?"
    r")\s*(?:,|$|})"
)
_LINTER_CONFIG_NAME = re.compile(
    r"(?i)(?:eslint|biome|stylelint|ruff|pylint|golangci|rubocop|swiftlint|ktlint|clippy|lint)"
)
_IGNORE_FILE_NAMES = {
    ".eslintignore",
    ".stylelintignore",
    ".biomeignore",
    ".prettierignore",
    ".ruffignore",
    ".mypyignore",
    ".pylintignore",
    ".flake8ignore",
    ".pyrightignore",
    ".tslintignore",
    ".golangciignore",
    ".rubocopignore",
    ".swiftlintignore",
    ".ktlintignore",
    ".clippyignore",
}
_TOOL_IGNORE_FILE = re.compile(
    r"(?i)(?:^|[._-])(?:eslint|stylelint|biome|prettier|ruff|mypy|pylint|flake8|pyright|"
    r"tslint|golangci(?:-lint)?|rubocop|swiftlint|ktlint|clippy|lint|check|test)"
    r"[._-]?ignore(?:$|[.])"
)
_GITIGNORE_RELEVANT_PATH = re.compile(
    r"(?i)(?:^|[/._*-])(?:src|source|app|apps|lib|libs|pkg|packages|"
    r"test(?:s|data)?|spec(?:s)?|check(?:s)?|lint(?:s)?|verify|typecheck|"
    r"scripts?|ci|workflow(?:s)?|tools?)(?:$|[/._*-])"
)
_GITIGNORE_SOURCE_EXTENSION = re.compile(
    r"(?i)\.(?:adb|asm|c|cc|cpp|cs|dart|ex|exs|fs|go|h|hpp|java|js|jsx|kt|lua|m|ml|php|pl|py|rb|rs|"
    r"css|less|sass|scss|sh|sql|swift|ts|tsx|vb|vue|xml|zig)(?:$|[/._*-])"
)
_DESTRUCTIVE_PATH_TOKEN = re.compile(
    r"(?i)(?:^|[/._-])(?:test(?:s|data|ing)?|spec(?:s)?|check(?:s)?|lint(?:s|ing)?|"
    r"verify|verification|typecheck|format|fmt)(?:$|[/._-])"
)
_SCRIPT_SUFFIXES = {
    ".bash",
    ".fish",
    ".js",
    ".mjs",
    ".cjs",
    ".ps1",
    ".py",
    ".rb",
    ".sh",
    ".ts",
    ".zsh",
}
_SCRIPT_MANIFEST_NAMES = {
    "build.gradle",
    "build.gradle.kts",
    "build.xml",
    "cargo.toml",
    "composer.json",
    "gemfile",
    "justfile",
    "makefile",
    "package.json",
    "pom.xml",
    "pyproject.toml",
    "rakefile",
    "taskfile.yml",
    "taskfile.yaml",
}
_SCRIPT_DIRECTORY_NAMES = {
    ".circleci",
    ".github",
    ".gitlab",
    "bin",
    "build",
    "ci",
    "scripts",
    "tools",
}
_PROVIDER_INVOCATION = re.compile(
    r"(?ix)(?:"
    r"\b(?:eslint|biome|tsc|pyright|mypy|ruff|pylint|flake8|pytest|jest|vitest|rubocop|"
    r"swiftlint|ktlint|golangci-lint)\b"
    r"|\b(?:cargo)\s+(?:fmt|clippy|check|test)\b"
    r"|\b(?:go)\s+(?:vet|test)\b"
    r"|\b(?:dotnet|mvn|gradle|swift|mix)\s+(?:test|check|verify|lint)\b"
    r"|\b(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?(?:lint|check|test|typecheck|verify)\b"
    r"|\b(?:make|just|task)\s+(?:lint|check|test|typecheck|verify)\b"
    r"|(?:(?:^|[\s\"'=:/])(?:\./)?(?:scripts?|bin|tools?)/[^\s\"']*"
    r"(?:lint|check|test|typecheck|verify)[^\s\"']*)"
    r")"
)
_PACKAGE_SCRIPT_KEY = re.compile(
    r"(?i)[\"'](?:lint|check|test|typecheck|verify)[\"']\s*:"
)
_PACKAGE_BYPASS = re.compile(r"\|\|\s*(?:true\b|:(?=\s|$|[\"']))")
_CHECK_EXIT_ZERO = re.compile(
    r"(?i)\b(?:ruff|eslint|stylelint|biome|mypy|pyright|pylint|flake8|golangci-lint|rubocop|swiftlint|ktlint)\b[^\n]*\s--exit-zero\b"
)
_DOWNGRADED_RULE = re.compile(
    r"(?ix)[\"']?[\w/@.*:-]+[\"']?\s*:\s*[\"']?(?:warn|warning)[\"']?(?:\s*[,}])"
)
_CI_DISABLED = re.compile(
    r"^\s*if\s*:\s*(?:false|\$\{\{\s*false\s*\}\})\s*$", re.IGNORECASE
)
_RULE_KEY_ONLY = re.compile(r"^\s*[\"']?[\w/@.*:-]+[\"']?\s*:\s*(?:#.*)?$")
_RULE_DISABLED_VALUE = re.compile(
    r"^\s*[\"']?(?:off|0|false)[\"']?\s*[,}]?\s*(?:#.*)?$", re.IGNORECASE
)
_CONFIG_KEY = re.compile(r"(?<![\w.-])[\"']?([\w.-]+)[\"']?\s*[:=]")
_HUNK_HEADER = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


@dataclass(frozen=True)
class _DiffEvent:
    path: Path
    kind: str
    line_number: int
    text: str = ""


def _comment_fragment(line: str, suffix: str) -> str | None:
    """Return a comment portion while ignoring quoted strings."""

    markers = ["//", "/*", "<!--"]
    if suffix in _HASH_COMMENT_SUFFIXES:
        markers.append("#")
    if suffix in _DASH_COMMENT_SUFFIXES:
        markers.append("--")
    if suffix in _PERCENT_COMMENT_SUFFIXES:
        markers.append("%")
    if suffix in _SEMICOLON_COMMENT_SUFFIXES:
        markers.append(";")
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char in {"'", '"', "`"}:
            quote = char
            index += 1
            continue
        for marker in markers:
            if line.startswith(marker, index):
                return line[index + len(marker) :]
        index += 1
    stripped = line.lstrip()
    if stripped.startswith("*"):
        return stripped[1:]
    return None


def _code_without_strings_or_comments(line: str, suffix: str) -> str:
    """Mask quotes/comments for shell and configuration command checks."""

    quote: str | None = None
    escaped = False
    output: list[str] = []
    index = 0
    while index < len(line):
        char = line[index]
        if quote is not None:
            output.append(" ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char in {"'", '"', "`"}:
            quote = char
            output.append(" ")
            index += 1
            continue
        if (
            (suffix in _HASH_COMMENT_SUFFIXES and char == "#")
            or (suffix in _DASH_COMMENT_SUFFIXES and line.startswith("--", index))
            or (suffix in _PERCENT_COMMENT_SUFFIXES and char == "%")
        ):
            break
        output.append(char)
        index += 1
    return "".join(output)


def _is_workflow(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    return (
        (".github" in parts and "workflows" in parts)
        or name.startswith(".gitlab-ci")
        or ".circleci" in parts
        or name
        in {
            "appveyor.yml",
            "azure-pipelines.yml",
            "azure-pipelines.yaml",
            "bitbucket-pipelines.yml",
            "buildkite.yml",
            "ci.yml",
            "ci.yaml",
            "jenkinsfile",
            ".travis.yml",
        }
        or ("ci" in parts and path.suffix.lower() in {".json", ".yaml", ".yml"})
    )


def _is_linter_config(path: Path) -> bool:
    name = path.name.lower()
    return (
        bool(_LINTER_CONFIG_NAME.search(name))
        or name.startswith((".eslintrc", ".stylelintrc", "tsconfig", ".golangci."))
        or name
        in {".flake8", "biome.json", "biome.jsonc", "mypy.ini", "pyproject.toml"}
        or "phpstan" in name
    )


def _is_comment_or_blank(line: str) -> bool:
    """Return whether an ignore/config line carries no active pattern."""

    stripped = line.strip()
    return not stripped or stripped.startswith(("#", ";", "//", "/*", "<!--", "--"))


def _is_ignore_file(path: Path) -> bool:
    """Recognize tool-specific ignore files whose patterns can hide checks."""

    name = path.name.lower()
    return name in _IGNORE_FILE_NAMES or bool(_TOOL_IGNORE_FILE.search(name))


def _is_relevant_gitignore_pattern(line: str) -> bool:
    """Return whether a Git ignore rule hides an authored/check-bearing path."""

    if _is_comment_or_blank(line):
        return False
    pattern = line.strip()
    if pattern.startswith("!"):
        return False
    # Ignore a trailing rationale while retaining escaped/hash-bearing paths.
    pattern = re.split(r"\s+#", pattern, maxsplit=1)[0].strip()
    return bool(
        _GITIGNORE_RELEVANT_PATH.search(pattern)
        or _GITIGNORE_SOURCE_EXTENSION.search(pattern)
    )


def _config_suppression(path: Path, line: str, section: str) -> str | None:
    """Recognize common config-level disables without treating all settings as waivers."""

    name = path.name.lower()
    for match in _CONFIG_KEY.finditer(line):
        key = match.group(1).lower().replace("-", "_")
        value = line[match.end() :].strip().lower()
        if (
            name.startswith("tsconfig")
            and key == "skiplibcheck"
            and re.match(r"(?:true|1|yes)\b", value)
        ):
            return "TypeScript library-check suppression"
        if (
            "golangci" in name
            and key == "disable_all"
            and re.match(r"(?:true|1|yes)\b", value)
        ):
            return "golangci-lint disable-all setting"
        if (
            ("mypy" in name or "mypy" in section)
            and key in {"ignore_errors", "ignore_missing_imports"}
            and re.match(r"(?:true|1|yes)\b", value)
        ):
            return "mypy error suppression setting"
        if (
            (name in {".flake8", "flake8", "setup.cfg"} or "flake8" in section)
            and key in {"ignore", "extend_ignore"}
            and value
        ):
            return "Flake8 ignored-rule setting"
        if (
            ("ruff" in section or "ruff" in name)
            and key in {"ignore", "extend_ignore", "exclude"}
            and value
        ):
            return "Ruff rule-selection/ignore setting"
        if (
            ("eslint" in section or "eslint" in name)
            and key in {"ignores", "ignorepatterns"}
            and value
        ):
            return "ESLint ignored-path setting"
        if "phpstan" in name and key in {"ignoreerrors", "ignore_errors"} and value:
            return "PHPStan baseline suppression setting"
        if (
            key in {"ignorepatterns", "ignore_pattern", "disable_all", "skip_lib_check"}
            and value
        ):
            return "linter suppression setting"
    return None


def _multiline_disabled_rule(lines: list[str], index: int) -> bool:
    if not _RULE_KEY_ONLY.match(lines[index]):
        return False
    for offset in range(index + 1, min(len(lines), index + 5)):
        if _RULE_DISABLED_VALUE.match(lines[offset]):
            return True
        if lines[offset].strip() and not lines[offset].strip().startswith(("#", "//")):
            break
    return False


def _json_brace_delta(line: str) -> int:
    masked = _code_without_strings_or_comments(line, ".json")
    return masked.count("{") - masked.count("}")


def _finding(
    path: Path, line_number: int, message: str, code: str = "lint-suppression"
) -> Finding:
    return Finding("error", code, path, f"line {line_number}: {message}", "suppression")
