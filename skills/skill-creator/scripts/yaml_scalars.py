"""Small, strict YAML scalar helpers used by the skill validator.

The validator intentionally supports the metadata subset used by Agent Skills
rather than depending on a third-party YAML parser.  Keeping scalar handling in
its own module lets the CLI facade and contract checks stay small while keeping
all direct imports from the original validator available through that facade.
"""

from __future__ import annotations

import json
import re
from typing import Any

YAML_NON_FINITE_FLOAT_RE = re.compile(
    r"(?P<sign>[+-]?)\.(?P<kind>inf|nan)", re.IGNORECASE
)
YAML_DECIMAL_INT_RE = re.compile(r"[-+]?[0-9](?:_?[0-9])*")
YAML_BINARY_INT_RE = re.compile(r"[-+]?0[bB][01](?:_?[01])*")
YAML_OCTAL_INT_RE = re.compile(r"[-+]?0[oO][0-7](?:_?[0-7])*")
YAML_HEX_INT_RE = re.compile(r"[-+]?0[xX][0-9a-fA-F](?:_?[0-9a-fA-F])*")
YAML_FLOAT_RE = re.compile(
    r"[-+]?(?:"
    r"[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?(?:[eE][-+]?[0-9](?:_?[0-9])*)?"
    r"|\.[0-9](?:_?[0-9])*(?:[eE][-+]?[0-9](?:_?[0-9])*)?"
    r"|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*"
    r")"
)
YAML_DECIMAL_CANDIDATE_RE = re.compile(
    r"[-+]?(?:[0-9][0-9_.eE+-]*|\.[0-9][0-9_.eE+-]*)"
)
YAML_BASE_PREFIX_RE = re.compile(r"[-+]?0[bBoOxX]")


def _consume_quoted(value: str, index: int, quote: str) -> tuple[int, str | None]:
    """Consume one character while scanning a single/double-quoted scalar."""
    character = value[index]
    if quote == "'":
        if character == "\\":
            raise ValueError(
                "Backslash-quote and other backslash escapes are not valid in a "
                "single-quoted YAML scalar; use '' for quotes."
            )
        if character == "'":
            if index + 1 < len(value) and value[index + 1] == "'":
                return index + 2, quote
            return index + 1, None
        return index + 1, quote
    if character == "\\":
        if index + 1 >= len(value):
            raise ValueError("Dangling backslash in double-quoted scalar.")
        # JSON-compatible escape validation is performed by _parse_scalar after
        # the surrounding mapping/flow boundaries have been identified.
        return index + 2, quote
    if character == '"':
        return index + 1, None
    return index + 1, quote


def _parse_quoted_scalar(value: str, quote: str) -> str:
    """Parse one complete quoted scalar, rejecting trailing text."""
    if not value or value[0] != quote:
        raise ValueError(f"Quoted scalar does not start with {quote!r}: {value!r}")
    index = 1
    while index < len(value):
        index, state = _consume_quoted(value, index, quote)
        if state is None:
            if index != len(value):
                raise ValueError(f"Trailing text after quoted scalar: {value!r}")
            if quote == "'":
                return value[1:-1].replace("''", "'")
            try:
                return json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid double-quoted scalar: {exc}") from exc
    raise ValueError(f"Unterminated quote in scalar: {value!r}")


def _starts_quote(value: str, index: int) -> bool:
    """Recognize a quoted scalar only at a YAML value/key boundary."""
    if value[index] not in {"'", '"'}:
        return False
    return index == 0 or value[index - 1].isspace() or value[index - 1] in "[{,:"


def _strip_inline_comment(value: str) -> str:
    quote: str | None = None
    index = 0
    while index < len(value):
        character = value[index]
        if quote is not None:
            index, quote = _consume_quoted(value, index, quote)
            continue
        if _starts_quote(value, index):
            quote = character
            index += 1
            continue
        if character == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
        index += 1
    if quote is not None:
        raise ValueError(f"Unterminated quote in scalar: {value!r}")
    return value.rstrip()


def _split_mapping_entry(value: str) -> tuple[str, str]:
    quote: str | None = None
    delimiters: list[str] = []
    separator: int | None = None
    index = 0
    while index < len(value):
        character = value[index]
        if quote is not None:
            index, quote = _consume_quoted(value, index, quote)
            continue
        if _starts_quote(value, index):
            quote = character
            index += 1
            continue
        if character in "[{":
            delimiters.append(character)
        elif character in "]}":
            expected = {"[": "]", "{": "}"}.get(delimiters[-1]) if delimiters else None
            if expected != character:
                raise ValueError(
                    f"Mismatched flow delimiters in mapping entry: {value!r}"
                )
            delimiters.pop()
        elif character == ":" and not delimiters and separator is None:
            separator = index
        index += 1
    if quote is not None:
        raise ValueError(f"Unterminated quote in mapping entry: {value!r}")
    if delimiters:
        raise ValueError(f"Unbalanced brackets in mapping entry: {value!r}")
    if separator is None:
        raise ValueError(f"Malformed frontmatter mapping entry: {value!r}")
    key = value[:separator].strip()
    if not key:
        raise ValueError(f"Empty mapping key: {value!r}")
    return key, value[separator + 1 :].strip()


def _split_flow_items(value: str) -> list[str]:
    if not value.strip():
        return []
    items: list[str] = []
    quote: str | None = None
    delimiters: list[str] = []
    start = 0
    index = 0
    while index < len(value):
        character = value[index]
        if quote is not None:
            index, quote = _consume_quoted(value, index, quote)
            continue
        if _starts_quote(value, index):
            quote = character
            index += 1
            continue
        if character in "[{":
            delimiters.append(character)
        elif character in "]}":
            expected = {"[": "]", "{": "}"}.get(delimiters[-1]) if delimiters else None
            if expected != character:
                raise ValueError(f"Mismatched flow delimiters in flow value: {value!r}")
            delimiters.pop()
        elif character == "," and not delimiters:
            item = value[start:index].strip()
            if not item:
                raise ValueError(f"Empty flow item around separator: {value!r}")
            items.append(item)
            start = index + 1
        index += 1
    if quote is not None:
        raise ValueError(f"Unterminated quote in flow value: {value!r}")
    if delimiters:
        raise ValueError(f"Unbalanced brackets in flow value: {value!r}")
    final_item = value[start:].strip()
    # A single final comma is valid YAML flow syntax.
    if final_item:
        items.append(final_item)
    elif not value.rstrip().endswith(","):
        raise ValueError(f"Empty flow item at end: {value!r}")
    return items


def _validate_plain_scalar(value: str, *, flow_context: bool = False) -> str:
    """Validate the narrow plain-scalar subset accepted by this parser."""
    if not value:
        return value
    if flow_context:
        if any(character in value for character in "[]{},"):
            raise ValueError(f"Unsupported punctuation in flow plain scalar: {value!r}")
        if ":" in value:
            raise ValueError(f"Colon is not supported in flow plain scalar: {value!r}")
    if value[0] in ":@`!&*%@|>},]":
        raise ValueError(f"Unsupported YAML plain-scalar indicator at start: {value!r}")
    if value[0] in "-?" and (len(value) == 1 or value[1].isspace()):
        raise ValueError(f"Unsupported YAML plain-scalar indicator at start: {value!r}")
    for index, character in enumerate(value[:-1]):
        if character == ":" and value[index + 1].isspace():
            raise ValueError(
                f"Colon followed by whitespace is not supported in plain scalar: {value!r}"
            )
    return value


def _parse_scalar(value: str, *, flow_context: bool = False) -> Any:
    value = _strip_inline_comment(value.strip())
    if value.startswith(("{", "[")):
        expected_close = "}" if value[0] == "{" else "]"
        if not value.endswith(expected_close):
            raise ValueError(f"Mismatched flow delimiters: {value!r}")
    if value.startswith(("'", '"')):
        return _parse_quoted_scalar(value, value[0])
    if value.startswith("!!str "):
        string_value = value[6:].strip()
        if string_value.startswith(("'", '"')):
            return _parse_quoted_scalar(string_value, string_value[0])
        return _validate_plain_scalar(string_value, flow_context=flow_context)
    if value in {"", "~", "null", "Null", "NULL"}:
        return None
    if value in {"true", "True", "TRUE", "false", "False", "FALSE"}:
        return value.casefold() == "true"
    non_finite_match = YAML_NON_FINITE_FLOAT_RE.fullmatch(value)
    if non_finite_match:
        if non_finite_match.group("kind").casefold() == "nan":
            return float("nan")
        return float("-inf") if non_finite_match.group("sign") == "-" else float("inf")
    if YAML_BINARY_INT_RE.fullmatch(value):
        return int(value.replace("_", ""), 2)
    if YAML_OCTAL_INT_RE.fullmatch(value):
        return int(value.replace("_", ""), 8)
    if YAML_HEX_INT_RE.fullmatch(value):
        return int(value.replace("_", ""), 16)
    if YAML_DECIMAL_INT_RE.fullmatch(value):
        return int(value.replace("_", ""), 10)
    if YAML_FLOAT_RE.fullmatch(value):
        return float(value.replace("_", ""))
    if YAML_BASE_PREFIX_RE.match(value) and not any(
        character.isspace() for character in value
    ):
        raise ValueError(f"Unsupported YAML numeric scalar: {value!r}")
    if YAML_DECIMAL_CANDIDATE_RE.fullmatch(value) and any(
        character in value for character in "._eE"
    ):
        raise ValueError(f"Unsupported YAML numeric scalar: {value!r}")
    if value.startswith("{") and value.endswith("}"):
        mapping: dict[Any, Any] = {}
        for item in _split_flow_items(value[1:-1].strip()):
            key, item_value = _split_mapping_entry(item)
            parsed_key = _parse_scalar(key, flow_context=True)
            if parsed_key in mapping:
                raise ValueError(f"Duplicate YAML mapping key: {parsed_key!r}")
            mapping[parsed_key] = _parse_scalar(item_value, flow_context=True)
        return mapping
    if value.startswith("[") and value.endswith("]"):
        return [
            _parse_scalar(item, flow_context=True)
            for item in _split_flow_items(value[1:-1].strip())
        ]
    return _validate_plain_scalar(value, flow_context=flow_context)


class _MetadataMap(dict[Any, Any]):
    def __init__(self) -> None:
        super().__init__()
        self.invalid_keys: list[Any] = []


def _next_content_line(lines: list[str], index: int, end: int) -> int:
    while index < end and (
        not lines[index].strip() or lines[index].lstrip().startswith("#")
    ):
        index += 1
    return index


def _leading_whitespace(line: str) -> str:
    """Return only indentation characters, excluding tabs in scalar content."""
    return line[: len(line) - len(line.lstrip(" \t"))]


def _reject_tab_indentation(lines: list[str], label: str) -> list[str]:
    """Report tabs used as indentation while allowing tabs in scalar content."""
    errors: list[str] = []
    for line_no, line in enumerate(lines, 1):
        if "\t" in _leading_whitespace(line):
            errors.append(
                f"{label} tab indentation is not supported on line {line_no}."
            )
    return errors


def _reject_yaml_control_characters(text: str, label: str) -> list[str]:
    """Reject control characters outside the YAML text subset we support."""
    errors: list[str] = []
    line_no = 1
    for character in text:
        codepoint = ord(character)
        c0_control = 0x00 <= codepoint <= 0x1F and codepoint not in {0x09, 0x0A, 0x0D}
        c1_control = 0x7F <= codepoint <= 0x9F
        if c0_control or c1_control:
            errors.append(
                f"{label} contains unsupported control character U+{codepoint:04X} "
                f"on line {line_no}."
            )
        if character == "\n":
            line_no += 1
    return errors


def _set_metadata_entry(metadata: _MetadataMap, key: Any, value: Any) -> None:
    try:
        if key in metadata:
            raise ValueError(f"Duplicate frontmatter metadata key: {key!r}")
        metadata[key] = value
    except TypeError:
        metadata.invalid_keys.append(key)
