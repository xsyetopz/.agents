"""BCP 47 validation, case normalization, and documented preferred mappings."""

from __future__ import annotations

import re
from collections.abc import Iterable

GRANDFATHERED_LOCALES = {
    "art-lojban",
    "cel-gaulish",
    "en-gb-oed",
    "i-ami",
    "i-bnn",
    "i-default",
    "i-enochian",
    "i-hak",
    "i-klingon",
    "i-lux",
    "i-mingo",
    "i-navajo",
    "i-pwn",
    "i-tao",
    "i-tay",
    "i-tsu",
    "no-bok",
    "no-nyn",
    "sgn-be-fr",
    "sgn-be-nl",
    "sgn-ch-de",
    "zh-guoyu",
    "zh-hakka",
    "zh-min",
    "zh-min-nan",
    "zh-xiang",
}
GRANDFATHERED_PREFERRED_VALUES = {
    "art-lojban": "jbo",
    "en-gb-oed": "en-GB-oxendict",
    "i-ami": "ami",
    "i-bnn": "bnn",
    "i-hak": "hak",
    "i-klingon": "tlh",
    "i-lux": "lb",
    "i-navajo": "nv",
    "i-pwn": "pwn",
    "i-tao": "tao",
    "i-tay": "tay",
    "i-tsu": "tsu",
    "no-bok": "nb",
    "no-nyn": "nn",
    "sgn-be-fr": "sfb",
    "sgn-be-nl": "vgt",
    "sgn-ch-de": "sgg",
    "zh-guoyu": "cmn",
    "zh-hakka": "hak",
    "zh-min-nan": "nan",
    "zh-xiang": "hsn",
}
LANGUAGE_PREFERRED_VALUES = {"iw": "he", "in": "id", "ji": "yi"}
SCRIPT_PREFERRED_VALUES = {"qaai": "Zinh"}
REGION_PREFERRED_VALUES = {
    "BU": "MM",
    "DD": "DE",
    "FX": "FR",
    "TP": "TL",
    "YD": "YE",
    "ZR": "CD",
}
LANGTAG_RE = re.compile(
    r"^(?:"
    r"(?:[A-Za-z]{2,3}(?:-[A-Za-z]{3}){0,3}|[A-Za-z]{4}|[A-Za-z]{5,8})"
    r"(?:-[A-Za-z]{4})?(?:-(?:[A-Za-z]{2}|[0-9]{3}))?"
    r"(?:-(?:[A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*"
    r"(?:-[0-9A-WY-Za-wy-z](?:-[A-Za-z0-9]{2,8})+)*"
    r"(?:-[xX](?:-[A-Za-z0-9]{1,8})+)?|[xX](?:-[A-Za-z0-9]{1,8})+)$"
)


def normalize_locale_tag(raw: str) -> str:
    value = raw.strip()
    lowered = value.lower()
    if lowered not in GRANDFATHERED_LOCALES and not LANGTAG_RE.fullmatch(value):
        raise ValueError(f"invalid BCP 47 locale: {raw}")
    if lowered in GRANDFATHERED_PREFERRED_VALUES:
        return GRANDFATHERED_PREFERRED_VALUES[lowered]
    if lowered in GRANDFATHERED_LOCALES or lowered.startswith("x-"):
        return lowered
    parts = value.split("-")
    language = parts[0].lower()
    normalized = [LANGUAGE_PREFERRED_VALUES.get(language, language)]
    extension_mode = False
    singletons: set[str] = set()
    variants: set[str] = set()
    for part in parts[1:]:
        if len(part) == 1 and part.isalnum():
            singleton = part.lower()
            if singleton in singletons:
                raise ValueError(
                    f"invalid BCP 47 locale with duplicate extension: {raw}"
                )
            singletons.add(singleton)
            extension_mode = True
            normalized.append(singleton)
        elif extension_mode:
            normalized.append(part.lower())
        elif (5 <= len(part) <= 8 and part.isalnum()) or (
            len(part) == 4 and part[0].isdigit() and part[1:].isalnum()
        ):
            variant = part.lower()
            if variant in variants:
                raise ValueError(f"invalid BCP 47 locale with duplicate variant: {raw}")
            variants.add(variant)
            normalized.append(variant)
        elif len(part) == 4 and part.isalpha():
            normalized.append(
                SCRIPT_PREFERRED_VALUES.get(part.casefold(), part.title())
            )
        elif (len(part) == 2 and part.isalpha()) or (len(part) == 3 and part.isdigit()):
            region = part.upper()
            normalized.append(REGION_PREFERRED_VALUES.get(region, region))
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def normalize_locales(values: Iterable[str]) -> list[str]:
    result = ["en"]
    seen = {"en"}
    for raw in values:
        locale = normalize_locale_tag(raw)
        key = locale.casefold()
        if key not in seen:
            result.append(locale)
            seen.add(key)
    return result
