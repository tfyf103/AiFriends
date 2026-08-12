#!/usr/bin/env python3
"""Structural internationalization and documentation-drift checks for AiFriends.

This checker deliberately focuses on facts a deterministic CI job can verify:
paired documents, Lab coverage, repository paths, required visual assets, canonical
terminology presence, and relative links. It does not pretend to judge whether a
translation is semantically perfect.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "i18n-manifest.json"
GLOSSARY = ROOT / "docs" / "BILINGUAL_GLOSSARY.md"

FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_RE = re.compile(r"\b(?:src|href)=[\"']([^\"']+)[\"']", re.IGNORECASE)
LAB_RE = re.compile(r"^chapter-(\d{2})-.*\.md$")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_manifest() -> dict:
    if not MANIFEST.exists():
        raise SystemExit("Missing docs/i18n-manifest.json")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def check_pairs(manifest: dict, errors: list[str]) -> list[Path]:
    checked: list[Path] = []
    for pair in manifest["document_pairs"]:
        zh = ROOT / pair["zh"]
        en = ROOT / pair["en"]
        for label, path in (("zh", zh), ("en", en)):
            if not path.is_file():
                fail(errors, f"Missing {label} paired document: {path.relative_to(ROOT)}")
            else:
                checked.append(path)
    return checked


def lab_chapters(directory: Path) -> set[str]:
    chapters: set[str] = set()
    if not directory.is_dir():
        return chapters
    for path in directory.iterdir():
        match = LAB_RE.match(path.name)
        if match:
            chapters.add(match.group(1))
    return chapters


def check_labs(errors: list[str]) -> list[Path]:
    zh_dir = ROOT / "labs"
    en_dir = ROOT / "labs" / "en"
    zh = lab_chapters(zh_dir)
    en = lab_chapters(en_dir)
    expected = {f"{n:02d}" for n in range(21)}

    if zh != expected:
        fail(errors, f"Chinese Labs drift: expected 00-20, found {sorted(zh)}")
    if en != expected:
        fail(errors, f"English Labs drift: expected 00-20, found {sorted(en)}")
    if zh != en:
        fail(errors, f"Bilingual Lab coverage differs: zh={sorted(zh)} en={sorted(en)}")

    return sorted(zh_dir.glob("chapter-*.md")) + sorted(en_dir.glob("chapter-*.md"))


def check_source_sentinels(manifest: dict, errors: list[str]) -> None:
    for item in manifest["source_sentinels"]:
        path = ROOT / item["path"]
        if not path.is_file():
            fail(errors, f"Documented source path disappeared: {item['path']}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        marker = item.get("contains")
        if marker and marker not in text:
            fail(errors, f"Source sentinel changed: {item['path']} no longer contains {marker!r}")


def check_assets(manifest: dict, errors: list[str]) -> None:
    for item in manifest["required_assets"]:
        if not (ROOT / item).is_file():
            fail(errors, f"Required bilingual/live-demo asset missing: {item}")


def check_glossary(manifest: dict, errors: list[str]) -> None:
    if not GLOSSARY.is_file():
        fail(errors, "Missing docs/BILINGUAL_GLOSSARY.md")
        return
    text = GLOSSARY.read_text(encoding="utf-8")
    for term in manifest["required_glossary_terms"]:
        if term not in text:
            fail(errors, f"Glossary missing canonical term: {term}")


def relative_targets(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    # Ignore code examples: paths inside fenced commands are not navigational links.
    text = FENCE_RE.sub("", text)
    return MARKDOWN_LINK_RE.findall(text) + HTML_SRC_RE.findall(text)


def normalize_target(raw: str) -> str | None:
    raw = raw.strip().split()[0].strip("<>\"'")
    if not raw or raw.startswith("#") or raw.startswith("//") or SCHEME_RE.match(raw):
        return None
    raw = unquote(raw).split("#", 1)[0].split("?", 1)[0]
    if not raw:
        return None
    # Site-root URLs such as /api/... are application routes, not repository files.
    if raw.startswith("/"):
        return None
    return raw


def check_links(paths: list[Path], errors: list[str]) -> None:
    seen: set[Path] = set()
    for path in paths:
        if not path.is_file() or path in seen:
            continue
        seen.add(path)
        for raw in relative_targets(path):
            target = normalize_target(raw)
            if target is None:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(errors, f"Link escapes repository: {path.relative_to(ROOT)} -> {raw}")
                continue
            if not resolved.exists():
                fail(errors, f"Broken relative link: {path.relative_to(ROOT)} -> {raw}")


def main() -> int:
    manifest = load_manifest()
    errors: list[str] = []

    pair_docs = check_pairs(manifest, errors)
    lab_docs = check_labs(errors)
    check_source_sentinels(manifest, errors)
    check_assets(manifest, errors)
    check_glossary(manifest, errors)

    important_docs = [
        ROOT / "README.md",
        ROOT / "README_EN.md",
        ROOT / "docs" / "README.md",
        ROOT / "docs" / "README_EN.md",
        ROOT / "docs" / "COURSE_REBUILD_EN.md",
        ROOT / "docs" / "BILINGUAL_GLOSSARY.md",
        ROOT / "docs" / "SCREENSHOTS.md",
        ROOT / "docs" / "LIVE_DEMO.md",
        ROOT / "docs" / "PRODUCT_EXPERIENCE.md",
        ROOT / "e2e" / "README.md",
    ]
    check_links(pair_docs + lab_docs + important_docs, errors)

    if errors:
        print("Internationalization/documentation checks FAILED:")
        for error in errors:
            print(f"  - {error}")
        print("\nThis checker verifies structural drift, not translation semantics.")
        return 1

    print("Internationalization/documentation checks passed")
    print("  - paired core documents present")
    print("  - Chinese/English Labs cover Chapter 00-20")
    print("  - documented source sentinels still exist")
    print("  - required live-demo assets present")
    print("  - canonical glossary terms present")
    print("  - important relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
