"""Validate the prompt-engineering model catalog and its routed guides."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "references" / "models"
CATALOG_PATH = MODEL_DIR / "catalog.json"

EVIDENCE_STATUSES = {
    "first-party-guidance",
    "shared-family-guidance",
    "engineering-guidance",
    "source-gap",
    "unverified",
}
CATALOG_FIELDS = {
    "requested_name",
    "provider",
    "provider_identifier",
    "normalized_slug",
    "guide_path",
    "language",
    "translation_status",
    "evidence_status",
    "source_urls",
    "source_record",
    "retrieved_at",
    "revision",
}
GUIDE_HEADINGS = {
    "en": ["Prompt recipe", "Operational constraints", "Sources"],
    "zh-CN": ["提示配方", "运行约束", "Sources"],
}
HTTPS_URL = re.compile(r"https://[^\s|)>`]+")
FIRST_PARTY_PREFIXES = (
    "https://developers.openai.com/",
    "https://docs.x.ai/",
    "https://help.aliyun.com/",
    "https://platform.minimax.io/",
    "https://www.minimax.io/",
    "https://docs.bigmodel.cn/",
    "https://docs.z.ai/",
    "https://platform.kimi.ai/",
    "https://www.kimi.com/",
    "https://api-docs.deepseek.com/",
    "https://mimo.xiaomi.com/",
    "https://github.com/QwenLM/",
    "https://github.com/MoonshotAI/",
    "https://github.com/deepseek-ai/",
    "https://huggingface.co/Qwen/",
    "https://huggingface.co/MoonshotAI/",
    "https://huggingface.co/deepseek-ai/",
)


def read_json(path: Path, label: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is not valid JSON: {exc}")
        return None


def safe_relative(raw: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        errors.append(f"{label} must be a non-empty relative path")
        return None
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label} leaves package root: {raw!r}")
        return None
    return path


def source_urls(text: str, label: str, errors: list[str]) -> list[str]:
    urls = [url.rstrip(".,;\"'") for url in HTTPS_URL.findall(text)]
    if not urls:
        errors.append(f"model guide has no HTTPS source: {label}")
    for url in urls:
        if not any(url.startswith(prefix) for prefix in FIRST_PARTY_PREFIXES):
            errors.append(f"non-first-party HTTPS source in {label}: {url}")
    return urls


def check_guide(entry: dict[str, object], errors: list[str]) -> None:
    raw_path = entry["guide_path"]
    path = ROOT / str(raw_path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"model guide cannot be read ({entry['requested_name']}): {exc}")
        return

    headings = re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    expected_headings = GUIDE_HEADINGS[str(entry["language"])]
    if headings != expected_headings:
        errors.append(f"model guide headings mismatch: {raw_path}")

    metadata = {
        "Provider": str(entry["provider"]),
        "Provider identifier": str(entry["provider_identifier"]),
        "Normalized slug": str(entry["normalized_slug"]),
        "Guide language": str(entry["language"]),
        "Translation status": str(entry["translation_status"]),
        "Evidence status": str(entry["evidence_status"]),
        "Retrieved": str(entry["retrieved_at"]),
        "Revision": str(entry["revision"]),
    }
    for label, value in metadata.items():
        pattern = rf"(?m)^- {re.escape(label)}:\s*(.+?)\s*$"
        match = re.search(pattern, text)
        if not match:
            errors.append(f"model guide metadata missing ({label}): {raw_path}")
        elif value not in match.group(1):
            errors.append(f"model guide metadata mismatch ({label}): {raw_path}")

    if not re.search(r"^#\s+.+", text, re.MULTILINE):
        errors.append(f"model guide has no title: {raw_path}")
    if str(entry["evidence_status"]) in {"source-gap", "unverified"}:
        status = str(entry["evidence_status"])
        if status not in text:
            errors.append(f"model guide lacks explicit {status} marker: {raw_path}")
        if (
            "do not infer" not in text.lower()
            and "不要据此推断" not in text
            and "不能据此推断" not in text
        ):
            errors.append(f"model guide lacks no-inference warning: {raw_path}")

    urls = source_urls(text, str(raw_path), errors)
    for url in entry["source_urls"]:  # type: ignore[union-attr]
        if str(url).rstrip(".,;") not in urls:
            errors.append(f"catalog source URL is absent from guide: {raw_path}: {url}")


def check_catalog(errors: list[str]) -> None:
    payload = read_json(CATALOG_PATH, "references/models/catalog.json", errors)
    if not isinstance(payload, dict):
        return
    if payload.get("schema_version") != 2:
        errors.append("model catalog schema_version must be 2")
    if payload.get("skill_name") != ROOT.name:
        errors.append("model catalog skill_name must match package name")
    statuses = payload.get("evidence_status_enum")
    if statuses != sorted(EVIDENCE_STATUSES):
        errors.append("model catalog evidence_status_enum must list the canonical statuses")

    entries = payload.get("models")
    if not isinstance(entries, list) or not entries:
        errors.append("model catalog models must be a non-empty array")
        return

    seen_slugs: set[str] = set()
    seen_paths: set[str] = set()
    previous_order: tuple[str, str] | None = None
    for index, raw in enumerate(entries):
        if not isinstance(raw, dict) or set(raw) != CATALOG_FIELDS:
            errors.append(f"model catalog entry {index} has non-canonical fields")
            continue
        for key in CATALOG_FIELDS - {"source_urls"}:
            if not isinstance(raw[key], str) or not raw[key].strip():
                errors.append(f"model catalog entry {index} has an empty {key}")
        urls = raw["source_urls"]
        if (
            not isinstance(urls, list)
            or not urls
            or any(not isinstance(url, str) or not url.startswith("https://") for url in urls)
        ):
            errors.append(f"model catalog entry {index} source_urls must be HTTPS strings")
        if raw["evidence_status"] not in EVIDENCE_STATUSES:
            errors.append(f"model catalog entry {index} has an invalid evidence_status")
        if raw["language"] not in {"en", "zh-CN"}:
            errors.append(f"model catalog entry {index} has an invalid language")
        if raw["translation_status"] not in {"original", "translated"}:
            errors.append(f"model catalog entry {index} has an invalid translation_status")
        if raw["language"] == "en" and raw["translation_status"] != "original":
            errors.append(f"English guide must be marked original: {raw['guide_path']}")
        if raw["language"] == "zh-CN" and raw["translation_status"] != "translated":
            errors.append(f"Chinese guide must be marked translated: {raw['guide_path']}")

        provider_slug = (
            str(raw["provider"]).casefold(),
            str(raw["normalized_slug"]).casefold(),
        )
        if previous_order is not None and provider_slug < previous_order:
            errors.append(f"model catalog order is not provider/slug sorted at {index}")
        previous_order = provider_slug
        slug = str(raw["normalized_slug"])
        if slug in seen_slugs:
            errors.append(f"duplicate normalized_slug: {slug}")
        seen_slugs.add(slug)

        path = safe_relative(raw["guide_path"], "model guide path", errors)
        if path is None or path.parent != Path("references/models") or path.suffix != ".md":
            errors.append(f"model guide path must stay under references/models: {raw['guide_path']}")
        elif not (ROOT / path).is_file():
            errors.append(f"missing model guide: {raw['guide_path']}")
        seen_paths.add(str(raw["guide_path"]))

        source_record = safe_relative(raw["source_record"], "source_record", errors)
        if source_record is None or not (ROOT / source_record).is_file():
            errors.append(f"missing source_record: {raw['source_record']}")
        check_guide(raw, errors)

    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in MODEL_DIR.glob("*.md")
        if path.name != "index.md"
    }
    if actual_paths != seen_paths:
        errors.append("references/models contains a guide not represented by catalog")


def check_model_index(errors: list[str]) -> None:
    path = MODEL_DIR / "index.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"references/models/index.md cannot be read: {exc}")
        return
    payload = read_json(CATALOG_PATH, "references/models/catalog.json", errors)
    if not isinstance(payload, dict) or not isinstance(payload.get("models"), list):
        return
    rows = [
        line
        for line in text.splitlines()
        if line.startswith("|") and line.count("|") >= 7 and "](" in line
    ]
    if len(rows) != len(payload["models"]):
        errors.append("model index row count must match catalog")
    links = re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)", text)
    normalized_links = {
        (Path("references/models") / target).as_posix()
        for target in links
        if not Path(target).is_absolute() and ".." not in Path(target).parts
    }
    expected_links = {str(entry["guide_path"]) for entry in payload["models"]}
    if normalized_links != expected_links:
        errors.append("model index links must cover exactly catalog guides")
    for entry in payload["models"]:
        line = next((row for row in rows if str(entry["requested_name"]) in row), "")
        if not line:
            errors.append(f"model index omits model: {entry['requested_name']}")
            continue
        for field in ("provider", "provider_identifier", "normalized_slug", "language", "translation_status", "evidence_status"):
            if str(entry[field]) not in line:
                errors.append(f"model index omits {field}: {entry['requested_name']}")


def check_model_catalog(errors: list[str]) -> None:
    check_catalog(errors)
    check_model_index(errors)
