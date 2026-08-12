from pathlib import Path


def insert_after(text: str, needle: str, insertion: str) -> str:
    if insertion.strip() in text:
        return text
    if needle not in text:
        raise RuntimeError(f"anchor not found: {needle}")
    return text.replace(needle, needle + insertion, 1)


def main() -> None:
    zh_path = Path("docs/README.md")
    en_path = Path("docs/README_EN.md")

    zh = zh_path.read_text(encoding="utf-8")
    en = en_path.read_text(encoding="utf-8")

    zh_row = "\n| [Product Experience / 实际产品体验](./PRODUCT_EXPERIENCE.md) | 从真实用户旅程理解 Character、Friend、Chat、Memory/RAG/Voice，并区分线上/E2E/源码/配置证据 |"
    zh = insert_after(
        zh,
        "| [Live Demo Verification](./LIVE_DEMO.md) | 线上截图真实性与只读验证记录 |",
        zh_row,
    )

    en_row = "\n| [PRODUCT_EXPERIENCE](./PRODUCT_EXPERIENCE.md) | Evidence-based real-user journey from Character discovery to Friend, Chat, Memory/RAG/Voice |"
    en = insert_after(
        en,
        "| [LIVE_DEMO](./LIVE_DEMO.md) | Real production screenshot verification |",
        en_row,
    )

    zh_path.write_text(zh, encoding="utf-8")
    en_path.write_text(en, encoding="utf-8")


if __name__ == "__main__":
    main()
