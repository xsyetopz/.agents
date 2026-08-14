"""Model-catalog validation for the prompt-engineering package."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HTTPS_URL = re.compile(r"https://[^\s|)>`]+")
FIRST_PARTY_URL_PREFIXES = (
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
    "https://github.com/openai/",
    "https://github.com/xai-org/",
    "https://github.com/QwenLM/",
    "https://github.com/MoonshotAI/",
    "https://github.com/deepseek-ai/",
    "https://huggingface.co/Qwen/",
    "https://huggingface.co/MoonshotAI/",
    "https://huggingface.co/deepseek-ai/",
)
MODEL_DIR = ROOT / "references" / "models"
MODEL_FIELDS = {
    "requested_name",
    "canonical_identifier",
    "guide_path",
    "language",
    "evidence_status",
}
MODEL_META = {
    "Qwen3.8-Max": (
        "qwen3.8-max",
        "zh-CN",
        "references/models/qwen3.8-max.zh-CN.md",
        "source gap",
    ),
    "GPT-5.6 family": (
        "gpt-5.6",
        "en",
        "references/models/gpt-5.6.en.md",
        "prompt guide (shared family)",
    ),
    "GPT-5.6 Sol": (
        "gpt-5.6-sol",
        "en",
        "references/models/gpt-5.6-sol.en.md",
        "prompt guide (shared family)",
    ),
    "GPT-5.6 Terra": (
        "gpt-5.6-terra",
        "en",
        "references/models/gpt-5.6-terra.en.md",
        "prompt guide (shared family)",
    ),
    "GPT-5.6 Luna": (
        "gpt-5.6-luna",
        "en",
        "references/models/gpt-5.6-luna.en.md",
        "prompt guide (shared family)",
    ),
    "Grok 4.6": ("grok-4.6", "en", "references/models/grok-4.6.en.md", "source gap"),
    "MiniMax M3": (
        "MiniMax-M3",
        "zh-CN",
        "references/models/minimax-m3.zh-CN.md",
        "prompt guide (M-series)",
    ),
    "GLM 5.2": (
        "glm-5.2",
        "zh-CN",
        "references/models/glm-5.2.zh-CN.md",
        "prompt guide",
    ),
    "Kimi K3": (
        "kimi-k3",
        "zh-CN",
        "references/models/kimi-k3.zh-CN.md",
        "prompt guide",
    ),
    "Qwen3.6-27B": (
        "Qwen3.6-27B",
        "zh-CN",
        "references/models/qwen3.6-27b.zh-CN.md",
        "source gap",
    ),
    "Qwen3.6 35B-A3B": (
        "Qwen3.6-35B-A3B",
        "zh-CN",
        "references/models/qwen3.6-35b-a3b.zh-CN.md",
        "source gap",
    ),
    "DeepSeek V4 Flash (0731)": (
        "deepseek-v4-flash",
        "zh-CN",
        "references/models/deepseek-v4-flash-0731.zh-CN.md",
        "API/engineering guidance",
    ),
    "DeepSeek V4 Pro (0813)": (
        "deepseek-v4-pro",
        "zh-CN",
        "references/models/deepseek-v4-pro-0813.zh-CN.md",
        "API/engineering guidance",
    ),
    "MiMo V2.5 Pro": (
        "mimo-v2.5-pro",
        "zh-CN",
        "references/models/mimo-v2.5-pro.zh-CN.md",
        "source gap",
    ),
    "MiMo V2.5": (
        "mimo-v2.5",
        "zh-CN",
        "references/models/mimo-v2.5.zh-CN.md",
        "source gap",
    ),
}
# Catalog statuses are compact English normalizations. These source-language
# markers make the normalization auditable without requiring identical prose.
GUIDE_STATUS_MARKERS = {
    "Qwen3.8-Max": ("来源缺口",),
    "GPT-5.6 family": ("prompt guide",),
    "GPT-5.6 Sol": ("prompt guide",),
    "GPT-5.6 Terra": ("prompt guide",),
    "GPT-5.6 Luna": ("prompt guide",),
    "Grok 4.6": ("source gap",),
    "MiniMax M3": ("提示指南",),
    "GLM 5.2": ("https://docs.bigmodel.cn/cn/guide/platform/prompt",),
    "Kimi K3": ("https://platform.kimi.ai/docs/guide/prompt-best-practice",),
    "Qwen3.6-27B": ("没有专属",),
    "Qwen3.6 35B-A3B": ("没有专属",),
    "DeepSeek V4 Flash (0731)": ("模型卡 + API/工程指南",),
    "DeepSeek V4 Pro (0813)": ("API/工程指南",),
    "MiMo V2.5 Pro": ("无独立提示指南",),
    "MiMo V2.5": ("无独立提示指南",),
}
MODEL_HEADINGS = {
    "en": ["Prompt recipe", "Operational constraints", "Official sources"],
    "zh-CN": ["提示配方", "运行约束", "官方来源"],
}


def safe_model_path(raw: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        errors.append(f"{label} must be a non-empty relative path")
        return None
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label} leaves package root: {raw!r}")
        return None
    return path


def read_model_json(path: Path, label: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is not valid JSON: {exc}")
        return None


def check_model_guide(entry: dict[str, str], errors: list[str]) -> None:
    name = entry["requested_name"]
    path = ROOT / entry["guide_path"]
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"model guide cannot be read ({name}): {exc}")
        return
    headings = re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    if headings != MODEL_HEADINGS[entry["language"]]:
        errors.append(f"model guide headings mismatch: {entry['guide_path']}")
    identifier = entry["canonical_identifier"]
    if not re.search(
        rf"(?:Canonical identifier:|规范标识：).*`?{re.escape(identifier)}`?",
        text,
    ):
        errors.append(f"model guide canonical ID mismatch: {entry['guide_path']}")
    if entry["language"] == "zh-CN":
        if "指南语言：简体中文" not in text:
            errors.append(f"model guide language marker missing: {entry['guide_path']}")
        if not re.search(r"[\u3400-\u9fff]", text):
            errors.append(f"zh-CN model guide lacks CJK text: {entry['guide_path']}")
    elif "Guide language: English" not in text:
        errors.append(
            f"English model guide language marker missing: {entry['guide_path']}"
        )
    check_source_urls(text, entry["guide_path"], errors)
    if "2026-08-14" not in text:
        errors.append(f"model guide lacks retrieval date: {entry['guide_path']}")
    markers = GUIDE_STATUS_MARKERS.get(name, ())
    if not any(marker in text for marker in markers):
        errors.append(f"model guide evidence status mismatch: {entry['guide_path']}")


def check_source_urls(text: str, label: str, errors: list[str]) -> None:
    urls = [url.rstrip(".,;") for url in HTTPS_URL.findall(text)]
    if not urls:
        errors.append(f"model guide has no first-party HTTPS source: {label}")
        return
    for url in urls:
        if not any(url.startswith(prefix) for prefix in FIRST_PARTY_URL_PREFIXES):
            errors.append(f"non-first-party HTTPS source in {label}: {url}")


def check_model_catalog(errors: list[str]) -> None:
    payload = read_model_json(
        ROOT / "references/models/catalog.json",
        "references/models/catalog.json",
        errors,
    )
    if not isinstance(payload, dict):
        return
    if payload.get("schema_version") != 1:
        errors.append("model catalog schema_version must be 1")
    if payload.get("skill_name") != ROOT.name:
        errors.append("model catalog skill_name must match package name")
    entries = payload.get("models")
    names = list(MODEL_META)
    if not isinstance(entries, list) or len(entries) != len(names):
        errors.append(f"model catalog must contain exactly {len(names)} entries")
        return
    guide_paths: list[str] = []
    checked: list[dict[str, str]] = []
    for index, raw in enumerate(entries):
        if not isinstance(raw, dict) or set(raw) != MODEL_FIELDS:
            errors.append(
                f"model catalog entry {index} must contain exactly the five model fields"
            )
            continue
        if any(
            not isinstance(raw[key], str) or not raw[key].strip()
            for key in MODEL_FIELDS
        ):
            errors.append(f"model catalog entry {index} has an empty field")
            continue
        name = raw["requested_name"]
        if index >= len(names) or name != names[index]:
            errors.append(f"model catalog requested_name order mismatch at {index}")
            continue
        expected = MODEL_META[name]
        if (
            tuple(
                raw[key]
                for key in (
                    "canonical_identifier",
                    "language",
                    "guide_path",
                    "evidence_status",
                )
            )
            != expected
        ):
            errors.append(f"model catalog metadata mismatch: {name}")
        relative = safe_model_path(raw["guide_path"], "model guide path", errors)
        if (
            relative is None
            or relative.suffix != ".md"
            or relative.parent != Path("references/models")
        ):
            errors.append(f"model guide path must stay under references/models: {name}")
        elif not (ROOT / relative).is_file():
            errors.append(f"missing model guide: {raw['guide_path']}")
        guide_paths.append(raw["guide_path"])
        checked.append(raw)
    expected_paths = [MODEL_META[name][2] for name in names]
    actual_paths = sorted(
        path.relative_to(ROOT).as_posix()
        for path in MODEL_DIR.glob("*.md")
        if path.name != "index.md"
    )
    if sorted(guide_paths) != sorted(expected_paths) or actual_paths != sorted(
        expected_paths
    ):
        errors.append(
            f"references/models must contain exactly the {len(expected_paths)} catalog guides"
        )
    index_path = MODEL_DIR / "index.md"
    try:
        index = index_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"references/models/index.md cannot be read: {exc}")
        return
    rows = [
        line for line in index.splitlines() if "](" in line and line.count("|") >= 5
    ]
    if len(rows) != len(names):
        errors.append(f"model index must contain one {len(names)}-row guide table")
    links = re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)", index)
    normalized_links = []
    for target in links:
        relative = safe_model_path(target, "model index link", errors)
        if relative is not None:
            normalized_links.append((Path("references/models") / relative).as_posix())
    if sorted(normalized_links) != sorted(expected_paths):
        errors.append(
            f"model index links must cover exactly the {len(expected_paths)} catalog guides"
        )
    for entry in checked:
        row = next((line for line in rows if entry["requested_name"] in line), "")
        language_label = "English" if entry["language"] == "en" else "简体中文"
        if not row or entry["canonical_identifier"] not in row:
            errors.append(
                f"model index omits catalog identity: {entry['requested_name']}"
            )
        if language_label not in row or entry["evidence_status"] not in row:
            errors.append(
                f"model index omits catalog metadata: {entry['requested_name']}"
            )
        check_model_guide(entry, errors)
