"""Conservative recognition and cleanup of the skill's old custom scaffold."""

from __future__ import annotations

import re
from pathlib import Path

from codeowners import is_owner
from file_operations import Operation, repo_path
from locales import normalize_locale_tag


LEGACY_PATHS = (
    ".github/ai-contribution-policy.yml",
    ".github/workflows/ai-contribution-policy.yml",
    ".github/ISSUE_TEMPLATE/agent-submitted.md",
    ".cursorrules",
    "llms.txt",
    "llms-full.txt",
)
LEGACY_MARKER = "repo-governance:"
LEGACY_TOKENS = (
    "HUMAN-AUTHORED",
    "AI-ASSISTED",
    "MAINTAINER-REQUESTED-AI",
    "USER-SUBMITTED",
    "AGENT-SUBMITTED",
)
LEGACY_BLOCKS = (
    (
        "<!-- repo-governance:start -->",
        "<!-- repo-governance:end -->",
    ),
    (
        "<!-- repo-governance:pr:start -->",
        "<!-- repo-governance:pr:end -->",
    ),
    (
        "<!-- repo-governance:readme:start -->",
        "<!-- repo-governance:readme:end -->",
    ),
    (
        "<!-- repo-governance:translation:start -->",
        "<!-- repo-governance:translation:end -->",
    ),
    (
        "# repo-governance:codeowners:start",
        "# repo-governance:codeowners:end",
    ),
)


FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})(.*)$")


def _unfenced_marker_spans(text: str, marker: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    offset = 0
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        fence = FENCE_RE.match(content)
        if fence_character is None:
            if fence:
                fence_character = fence.group(1)[0]
                fence_length = len(fence.group(1))
            elif content.strip() == marker:
                spans.append((offset, offset + len(line)))
        elif (
            fence
            and fence.group(1)[0] == fence_character
            and len(fence.group(1)) >= fence_length
            and not fence.group(2).strip()
        ):
            fence_character = None
            fence_length = 0
        offset += len(line)
    return spans


ROOT_BLOCK_LINES = (
    "## AI / Coding Agents",
    "AI-ASSISTED USER-SUBMITTED AGENT-SUBMITTED",
)
PR_BLOCK_LINES = (
    "## Contribution origin",
    "HUMAN-AUTHORED or AI-ASSISTED",
    "## Submission actor",
    "USER-SUBMITTED or AGENT-SUBMITTED",
    "## Verification",
    "- [ ] Verified.",
)
README_BLOCK_LINES = (
    "## AI / Coding Agents",
    "Read CONTRIBUTING.md, AGENTS.md, and llms.txt.",
    "AI-ASSISTED USER-SUBMITTED",
)
CODEOWNER_BLOCK_PATHS = (
    "/AGENTS.md",
    "/CLAUDE.md",
    "/GEMINI.md",
    "/.cursor/rules/agents.mdc",
    "/llms.txt",
    "/llms-full.txt",
    "/.github/ai-contribution-policy.yml",
    "/.github/pull_request_template.md",
    "/.github/workflows/ai-contribution-policy.yml",
)


def _translation_block_matches(lines: list[str]) -> bool:
    if len(lines) != 3:
        return False
    heading = re.fullmatch(
        r"# AI / Coding Agents(?: \(([^)]+)\)| — ([^\s]+))", lines[0]
    )
    if not heading or not re.fullmatch(r"Source policy: [^\r\n]+", lines[1]):
        return False
    try:
        normalize_locale_tag(heading.group(1) or heading.group(2))
    except ValueError:
        return False
    return lines[2] == "AI-ASSISTED USER-SUBMITTED"


def _codeowner_block_matches(lines: list[str]) -> bool:
    if len(lines) != len(CODEOWNER_BLOCK_PATHS):
        return False
    owners: list[str] = []
    for line, expected_path in zip(lines, CODEOWNER_BLOCK_PATHS, strict=True):
        parts = line.split()
        if len(parts) != 2 or parts[0] != expected_path or not is_owner(parts[1]):
            return False
        owners.append(parts[1])
    return len(set(owners)) == 1


def _inline_body_matches(start: str, body: str) -> bool:
    lines = body.strip("\r\n").splitlines()
    if start == "<!-- repo-governance:start -->":
        return lines == list(ROOT_BLOCK_LINES)
    if start == "<!-- repo-governance:pr:start -->":
        return lines == list(PR_BLOCK_LINES)
    if start == "<!-- repo-governance:readme:start -->":
        return lines == list(README_BLOCK_LINES)
    if start == "<!-- repo-governance:translation:start -->":
        return _translation_block_matches(lines)
    if start == "# repo-governance:codeowners:start":
        return _codeowner_block_matches(lines)
    return False


def strip_legacy_blocks(text: str) -> str:
    """Remove only unfenced, structurally recognized old generated blocks."""
    for start, end in LEGACY_BLOCKS:
        starts = _unfenced_marker_spans(text, start)
        ends = _unfenced_marker_spans(text, end)
        if not starts and not ends:
            continue
        if len(starts) != 1 or len(ends) != 1 or starts[0][0] >= ends[0][0]:
            raise ValueError(f"unbalanced or duplicate legacy markers: {start}, {end}")
        body = text[starts[0][1] : ends[0][0]]
        if not _inline_body_matches(start, body):
            raise ValueError(
                f"legacy markers have an unrecognized or incomplete body: {start}, {end}"
            )
        text = text[: starts[0][0]] + text[ends[0][1] :]
    return text.strip() + "\n" if text.strip() else ""


def legacy_candidates(root: Path) -> list[Path]:
    paths = [repo_path(root, relative) for relative in LEGACY_PATHS]
    docs = root / "docs"
    if docs.is_dir() and not docs.is_symlink():
        paths.extend(sorted(docs.glob("ai-contribution-policy.*.md")))
    return [path for path in paths if path.exists() or path.is_symlink()]


def recognized_legacy(path: Path, root: Path) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError:
        return False
    relative = path.relative_to(root).as_posix()
    lines = set(text.splitlines())
    html_marker = "<!-- repo-governance:file -->" in lines
    yaml_marker = "# repo-governance:file" in lines
    token_count = sum(token in text for token in LEGACY_TOKENS)
    if relative == ".github/ai-contribution-policy.yml":
        return (
            yaml_marker
            and all(
                re.search(rf"(?m)^{re.escape(field)}", text)
                for field in (
                    "schema_version: 1",
                    "policy_version: 1",
                    "canonical_locale: en",
                    "mode:",
                    "origin_tokens:",
                    "submission_actor_tokens:",
                    "required_check:",
                )
            )
            and token_count >= 2
        )
    if relative == ".github/workflows/ai-contribution-policy.yml":
        return (
            yaml_marker
            and "name: AI contribution policy" in text
            and "pull_request_target:" in text
            and "contents: read" in text
            and "pull-requests: read" in text
            and all(
                variable in text
                for variable in ("PR_TITLE:", "PR_BODY:", "PR_LABELS_JSON:")
            )
            and token_count >= 2
        )
    if relative == ".github/ISSUE_TEMPLATE/agent-submitted.md":
        return (
            html_marker
            and text.startswith("---\n")
            and "name: Agent-submitted issue" in text
            and "AGENT-SUBMITTED" in text
            and "Authorization scope" in text
            and "## Verification" in text
            and "- [ ]" in text
        )
    if relative == ".cursorrules":
        lowered = text.casefold()
        return (
            html_marker
            and "# Canonical repository instructions" in lines
            and "AGENTS.md" in text
            and "nearest nested" in lowered
            and "canonical rules" in lowered
        )
    if relative == "llms.txt":
        return (
            html_marker
            and "## Agent guidance" in lines
            and "AGENTS.md" in text
            and "llms-full.txt" in text
            and ".github/pull_request_template.md" in text
            and "## Localized policy" in lines
        )
    if relative == "llms-full.txt":
        return html_marker and all(
            heading in lines
            for heading in (
                "## Authority and scope",
                "## Required workflow",
                "## AI contribution policy",
                "## Localized policy",
            )
        )
    if relative.startswith("docs/ai-contribution-policy.") and relative.endswith(".md"):
        return (
            "<!-- repo-governance:translation:start -->" in lines
            and "<!-- repo-governance:translation:end -->" in lines
            and any(
                "AI / Coding Agents" in line and line.lstrip().startswith("#")
                for line in lines
            )
            and "Source policy:" in text
            and token_count >= 2
        )
    return False


def plan_legacy(root: Path) -> list[Operation]:
    return [
        Operation(path, "delete", reason="recognized legacy scaffold artifact")
        for path in legacy_candidates(root)
        if recognized_legacy(path, root)
    ]


def validate_no_legacy(root: Path) -> list[str]:
    errors = [
        f"recognized legacy artifact remains: {path.relative_to(root).as_posix()}"
        for path in legacy_candidates(root)
        if recognized_legacy(path, root)
    ]
    for relative in (
        "CONTRIBUTING.md",
        "AGENTS.md",
        ".github/pull_request_template.md",
        ".github/CODEOWNERS",
    ):
        path = repo_path(root, relative)
        if path.is_file() and not path.is_symlink():
            text = path.read_text(encoding="utf-8")
            markers = [marker for pair in LEGACY_BLOCKS for marker in pair]
            markers.extend(
                (
                    "<!-- repo-governance:file -->",
                    "# repo-governance:file",
                )
            )
            residual = any(_unfenced_marker_spans(text, marker) for marker in markers)
        else:
            residual = False
        if residual:
            errors.append(
                f"legacy scaffold marker remains in governed file: {relative}"
            )
    return errors
