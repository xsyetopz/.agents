"""Validation for the package's optional ``agents/openai.yaml`` metadata."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from yaml_scalars import (
    _parse_scalar,
    _reject_tab_indentation,
    _reject_yaml_control_characters,
    _split_mapping_entry,
)


def _check_yaml_top_level_syntax(lines: list[str], errors: list[str]) -> list[str]:
    """Reject malformed top-level YAML instead of extracting around it."""
    top_level_keys: list[str] = []
    seen_top_level: set[str] = set()
    allow_indented = False
    for line_no, raw in enumerate(lines, 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" \t"))
        if indent:
            if not allow_indented:
                errors.append(
                    f"agents/openai.yaml unexpected indentation on line {line_no}."
                )
            continue
        try:
            key, value = _split_mapping_entry(raw.strip())
        except ValueError as exc:
            errors.append(
                f"agents/openai.yaml malformed top-level YAML on line {line_no}: {exc}"
            )
            allow_indented = False
            continue
        if not key.strip():
            errors.append(f"agents/openai.yaml empty top-level key on line {line_no}.")
            allow_indented = False
            continue
        if key in seen_top_level:
            errors.append(
                f"agents/openai.yaml duplicate top-level key {key!r} on line {line_no}."
            )
        else:
            seen_top_level.add(key)
            top_level_keys.append(key)
        if value:
            try:
                _parse_scalar(value)
            except (TypeError, ValueError) as exc:
                errors.append(
                    f"agents/openai.yaml malformed value for {key!r} on line "
                    f"{line_no}: {exc}"
                )
        allow_indented = not value or value in {">", ">-", ">+", "|", "|-", "|+"}
    return top_level_keys


def check_agents_yaml(root: Path, errors: list[str]) -> None:
    """Validate agents/openai.yaml structure and routing metadata."""
    yaml_path = root / "agents" / "openai.yaml"
    if not yaml_path.is_file():
        return
    try:
        text = yaml_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"Unable to read agents/openai.yaml: {exc}")
        return
    control_errors = _reject_yaml_control_characters(text, "agents/openai.yaml")
    if control_errors:
        errors.extend(control_errors)
        return
    lines = text.splitlines()
    tab_errors = _reject_tab_indentation(lines, "agents/openai.yaml")
    if tab_errors:
        errors.extend(tab_errors)
        return
    _check_yaml_top_level_syntax(lines, errors)
    interface_index: int | None = None
    for index, line in enumerate(lines):
        if line.startswith((" ", "\t")):
            continue
        try:
            key, _value = _split_mapping_entry(line.strip())
        except ValueError:
            continue
        if key == "interface":
            interface_index = index
            break
    if interface_index is None:
        errors.append("agents/openai.yaml is missing required 'interface:' key.")
        return

    interface_indent = len(lines[interface_index]) - len(
        lines[interface_index].lstrip(" \t")
    )
    try:
        _interface_key, interface_value = _split_mapping_entry(
            lines[interface_index].strip()
        )
    except ValueError:
        errors.append("agents/openai.yaml has malformed 'interface:' mapping.")
        return

    fields: dict[str, Any] = {}
    malformed = False
    if interface_value:
        try:
            parsed_interface = _parse_scalar(interface_value)
        except (TypeError, ValueError) as exc:
            errors.append(
                f"agents/openai.yaml has malformed 'interface:' mapping: {exc}"
            )
            parsed_interface = None
            malformed = True
        if isinstance(parsed_interface, dict):
            fields.update(parsed_interface)
        elif parsed_interface is not None:
            errors.append("agents/openai.yaml 'interface:' must be a mapping.")
            malformed = True
    cursor = interface_index + 1
    while cursor < len(lines):
        raw = lines[cursor]
        if not raw.strip() or raw.lstrip().startswith("#"):
            cursor += 1
            continue
        indent = len(raw) - len(raw.lstrip(" \t"))
        if indent <= interface_indent:
            break
        try:
            key, value = _split_mapping_entry(raw.strip())
        except ValueError as exc:
            errors.append(
                f"agents/openai.yaml malformed interface field on line {cursor + 1}: {exc}"
            )
            malformed = True
            cursor += 1
            continue
        if key in fields:
            errors.append(f"agents/openai.yaml has duplicate interface field: {key!r}.")
            cursor += 1
            continue
        cursor += 1
        if value in {">", ">-", ">+", "|", "|-", "|+"}:
            block: list[str] = []
            while cursor < len(lines):
                block_line = lines[cursor]
                block_indent = len(block_line) - len(block_line.lstrip(" \t"))
                if block_line.strip() and block_indent <= indent:
                    break
                block.append(block_line.strip())
                cursor += 1
            if value.startswith(">"):
                fields[key] = " ".join(part for part in block if part)
            else:
                fields[key] = "\n".join(block).strip()
        else:
            try:
                fields[key] = _parse_scalar(value)
            except (TypeError, ValueError) as exc:
                errors.append(
                    f"agents/openai.yaml interface field {key!r} is malformed: {exc}"
                )
                malformed = True
    if malformed:
        errors.append("agents/openai.yaml has malformed interface metadata.")

    display_name = fields.get("display_name")
    if not isinstance(display_name, str) or not display_name.strip():
        errors.append("agents/openai.yaml is missing required 'display_name'.")

    short_description = fields.get("short_description")
    if not isinstance(short_description, str) or not short_description.strip():
        errors.append("agents/openai.yaml is missing required 'short_description'.")
    elif not 25 <= len(short_description) <= 64:
        errors.append(
            "agents/openai.yaml short_description must be 25-64 characters "
            f"(got {len(short_description)})."
        )

    default_prompt = fields.get("default_prompt")
    if not isinstance(default_prompt, str) or not default_prompt.strip():
        errors.append("agents/openai.yaml is missing required 'default_prompt'.")
    else:
        expected = f"${root.name}"
        if expected not in default_prompt:
            errors.append(f"agents/openai.yaml default_prompt must mention {expected}.")
        elif re.findall(r"\$[a-z0-9-]+", default_prompt) != [expected]:
            errors.append(
                f"agents/openai.yaml default_prompt must invoke exactly {expected}."
            )


__all__ = ["check_agents_yaml"]
