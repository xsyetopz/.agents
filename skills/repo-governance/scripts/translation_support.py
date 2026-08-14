"""Reviewed translation input and repository locale discovery."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from legacy_artifacts import LEGACY_MARKER, LEGACY_TOKENS
from locales import normalize_locale_tag


def parse_translations(values: Iterable[str], label: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"{label} must use LOCALE=/absolute/path: {value}")
        raw_locale, raw_path = value.split("=", 1)
        locale = normalize_locale_tag(raw_locale)
        path = Path(raw_path)
        if locale == "en":
            raise ValueError(f"English uses the root files, not {label}")
        if not path.is_absolute() or not path.is_file() or path.is_symlink():
            raise ValueError(
                f"{label} must name an existing absolute regular file: {raw_path}"
            )
        if locale in result:
            raise ValueError(f"duplicate {label} for locale: {locale}")
        result[locale] = path
    return result


def reviewed_content(locale: str, path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text or "\x00" in text:
        raise ValueError(f"reviewed translation for {locale} is empty or invalid")
    if LEGACY_MARKER in text or any(token in text for token in LEGACY_TOKENS):
        raise ValueError(
            f"reviewed translation for {locale} contains a legacy protocol"
        )
    return text


def discover_locales(root: Path) -> list[str]:
    location = root / "docs/i18n"
    if location.is_symlink():
        raise ValueError("docs/i18n must not be a symlink")
    if location.exists() and not location.is_dir():
        raise ValueError("docs/i18n must be a directory")
    result: list[str] = []
    seen: set[str] = set()
    if not location.exists():
        return result
    for child in sorted(location.iterdir(), key=lambda item: item.name):
        if child.is_symlink():
            raise ValueError(f"locale directory must not be a symlink: {child.name}")
        if not child.is_dir():
            continue
        locale = normalize_locale_tag(child.name)
        if locale != child.name or locale == "en":
            raise ValueError(
                f"locale directory must use its normalized non-English BCP 47 tag: "
                f"{child.name} -> {locale}"
            )
        if locale.casefold() in seen:
            raise ValueError(f"duplicate normalized locale directory: {locale}")
        seen.add(locale.casefold())
        result.append(locale)
    return result
