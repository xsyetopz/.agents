"""Frontmatter parser for the package-local skill validator."""

from __future__ import annotations

from typing import Any

from yaml_scalars import (
    _MetadataMap,
    _next_content_line,
    _parse_scalar,
    _reject_tab_indentation,
    _reject_yaml_control_characters,
    _set_metadata_entry,
    _split_mapping_entry,
)


def _parse_metadata_mapping(
    lines: list[str], index: int, end: int, indent: int | None = None
) -> tuple[_MetadataMap, int]:
    index = _next_content_line(lines, index, end)
    if index >= end:
        return _MetadataMap(), index

    if indent is None:
        indent = len(lines[index]) - len(lines[index].lstrip(" \t"))
        if indent == 0:
            return _MetadataMap(), index
    metadata = _MetadataMap()

    while True:
        index = _next_content_line(lines, index, end)
        if index >= end:
            break
        raw = lines[index]
        raw_indent = len(raw) - len(raw.lstrip(" \t"))
        if raw_indent < indent:
            break
        if raw_indent > indent:
            raise ValueError("Malformed frontmatter metadata indentation.")

        key_text, value_text = _split_mapping_entry(raw.strip())
        key = _parse_scalar(key_text)
        index += 1

        if value_text in {">", ">-", ">+", "|", "|-", "|+"}:
            scalar_style = value_text[0]
            scalar_lines: list[str] = []
            while index < end and (
                not lines[index].strip()
                or (
                    lines[index].startswith((" ", "\t"))
                    and len(lines[index]) - len(lines[index].lstrip(" \t")) > indent
                )
            ):
                scalar_lines.append(lines[index].strip())
                index += 1
            if scalar_style == ">":
                value: Any = " ".join(part for part in scalar_lines if part)
            else:
                value = "\n".join(scalar_lines).strip()
        elif value_text:
            value = _parse_scalar(value_text)
        else:
            child_index = _next_content_line(lines, index, end)
            if child_index < end:
                child_indent = len(lines[child_index]) - len(
                    lines[child_index].lstrip(" \t")
                )
            else:
                child_indent = indent
            if child_index < end and child_indent > indent:
                value, index = _parse_metadata_mapping(
                    lines, child_index, end, child_indent
                )
            else:
                value = None
                index = child_index

        _set_metadata_entry(metadata, key, value)

    return metadata, index


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    raw_lines = text.splitlines(keepends=True)
    if not raw_lines or raw_lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")
    try:
        end = next(i for i in range(1, len(raw_lines)) if raw_lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter has no closing '---'.") from exc
    control_errors = _reject_yaml_control_characters(
        "".join(raw_lines[: end + 1]), "SKILL.md frontmatter"
    )
    if control_errors:
        raise ValueError(control_errors[0])

    lines = text.splitlines()
    tab_errors = _reject_tab_indentation(lines[: end + 1], "SKILL.md frontmatter")
    if tab_errors:
        raise ValueError(tab_errors[0])

    data: dict[str, Any] = {}
    index = 1
    while index < end:
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#"):
            index += 1
            continue
        if raw.startswith((" ", "\t")):
            raise ValueError(
                f"Malformed frontmatter: unexpected indentation on line {index + 1}."
            )
        try:
            key, value = _split_mapping_entry(raw)
        except ValueError as exc:
            raise ValueError(
                f"Malformed frontmatter mapping on line {index + 1}: {exc}"
            ) from exc
        if not key.strip():
            raise ValueError(f"Malformed frontmatter: empty key on line {index + 1}.")
        if value in {">", ">-", ">+", "|", "|-", "|+"}:
            scalar_style = value[0]
            scalar_lines: list[str] = []
            index += 1
            while index < end and (
                not lines[index].strip() or lines[index].startswith((" ", "\t"))
            ):
                scalar_lines.append(lines[index].strip())
                index += 1
            if scalar_style == ">":
                value = " ".join(part for part in scalar_lines if part)
            else:
                value = "\n".join(scalar_lines).strip()
            if key in data:
                raise ValueError(f"Duplicate frontmatter key: {key!r}")
            data[key] = value
        elif key == "metadata" and not value:
            index += 1
            if key in data:
                raise ValueError(f"Duplicate frontmatter key: {key!r}")
            data[key], index = _parse_metadata_mapping(lines, index, end)
        else:
            if key in data:
                raise ValueError(f"Duplicate frontmatter key: {key!r}")
            data[key] = _parse_scalar(value)
            index += 1
    return data, "\n".join(lines[end + 1 :])


__all__ = ["parse_frontmatter"]
