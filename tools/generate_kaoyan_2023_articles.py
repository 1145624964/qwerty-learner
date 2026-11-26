from __future__ import annotations

import json
import pathlib
import re
from typing import Any

from kaoyan_articles_spec import (
    ARTICLES_JSON_OUT,
    ARTICLES_SPEC,
    DESKTOP_ARTICLE_DIR,
    DICT_PATH,
    REPO_ROOT,
    count_english_words,
)


def render_clean_article_markdown(art: dict[str, Any]) -> str:
    """Render clean reading article without any boilerplate/metadata preamble or calibration footer."""
    lines: list[str] = [
        f"# {art['group']}第{art['groupDay']}天 · 文章{art['articleNumber']}",
        "",
        f"## {art['title']}",
        "",
        "## 英文原文",
        "",
    ]

    for idx, (en_p, _) in enumerate(art["paragraphs"], 1):
        lines.append(f"[P{idx}] {en_p}")
        lines.append("")

    lines.append("## 阅读理解")
    lines.append("")
    for q in art["questions"]:
        lines.append(f"{q['ordinal']}. {q['stem']}")
        for opt in q["options"]:
            lines.append(f"   - {opt}")
        lines.append("")

    lines.extend(
        [
            "## 本文目标词释义",
            "",
            "| 当日序号 | 原词 | 本文形式与位置 | 本文释义、搭配与辨析 |",
            "| ---: | --- | --- | --- |",
        ]
    )
    for g in art["glossary"]:
        lines.append(
            f"| {g['dayOrder']} | {g['word']} | {g['surface']}；本文 {g['para']} | {g['meaning']} |"
        )
    lines.append("")

    if art.get("crossovers"):
        lines.extend(
            [
                "## 当日词复现",
                "",
                "| 原词 | 本文位置 | 本文义项与搭配 |",
                "| --- | --- | --- |",
            ]
        )
        for c in art["crossovers"]:
            lines.append(f"| {c['word']} | {c['para']} | {c['meaning']} |")
        lines.append("")

    ans_summary = "，".join(f"{q['ordinal']} {q['answer']}" for q in art["questions"])
    lines.extend(
        [
            "## 答案与解析",
            "",
            f"答案：{ans_summary}。",
            "",
        ]
    )
    for q in art["questions"]:
        lines.append(f"{q['ordinal']}. **{q['answer']}｜** {q['explanation']}")
        lines.append("")

    lines.extend(
        [
            "## 长难句精读",
            "",
        ]
    )
    for idx, s in enumerate(art["sentences"], 1):
        lines.append(f"{idx}. “{s['sentence']}”")
        lines.append(f"   - {s['analysis']}")
        lines.append("")

    lines.extend(
        [
            "## 完整译文",
            "",
            art["zhTitle"],
            "",
        ]
    )
    for idx, (_, zh_p) in enumerate(art["paragraphs"], 1):
        lines.append(f"[P{idx}] {zh_p}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def clean_existing_markdown_file(md_path: pathlib.Path) -> str:
    """Strip non-essential boilerplate lines and ## 来源与校准 section from an existing article markdown."""
    raw = md_path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    out: list[str] = []
    skip_section = False

    for line in lines:
        s = line.strip()
        if s.startswith("## 来源与校准"):
            skip_section = True
            continue
        if skip_section:
            if s.startswith("## "):
                skip_section = False
            else:
                continue

        # Remove OCR disclaimer quotes or boilerplate lines
        if s.startswith("> 本文件由扫描PDF做OCR转录"):
            continue
        if s.startswith("计划日期：") and "正文：" in s:
            continue
        if s.startswith("本篇为原创、") and "风格强化练习" in s:
            continue
        if s.startswith("序号沿用当天") and ("位置指英文原文段落" in s or "先解释本文义项" in s):
            continue
        if s.startswith("以下词也来自当天词表，已在另一篇主词表中列出"):
            continue

        out.append(line)

    # Collapse 3+ consecutive blank lines into single blank line
    cleaned = "\n".join(out)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip() + "\n"
    md_path.write_text(cleaned, encoding="utf-8")
    return cleaned


def main() -> None:
    dict_entries = json.loads(DICT_PATH.read_text("utf-8"))
    DESKTOP_ARTICLE_DIR.mkdir(parents=True, exist_ok=True)

    by_chap: dict[str, list[dict[str, Any]]] = {}
    wc_errors: list[str] = []
    for art in ARTICLES_SPEC:
        wc = count_english_words(art["paragraphs"])
        art["wordCount"] = wc
        by_chap.setdefault(art["chapterId"], []).append(art)
        print(f"{art['id']} ({art['title']}): {wc} words, {len(art['glossary'])} target words")
        if not (455 <= wc <= 525):
            wc_errors.append(f"Word count {wc} out of expected 455..525 range for {art['id']}")

    chapters = json.loads((REPO_ROOT / "src" / "resources" / "shanguo_kaoyan_2023_chapters.json").read_text("utf-8"))
    chap_map = {c["id"]: c for c in chapters}

    for cid, arts in by_chap.items():
        chap = chap_map[cid]
        expected_entries = dict_entries[chap["start"] : chap["end"]]
        total_day_words = len(expected_entries)
        covered_orders = {}
        for art in arts:
            en_full = "\n".join(p[0] for p in art["paragraphs"])
            for g in art["glossary"]:
                order = g["dayOrder"]
                assert order not in covered_orders, f"Duplicate dayOrder {order} in {cid}"
                covered_orders[order] = g["word"]
                expected_word = expected_entries[order - 1]["name"]
                assert g["word"].lower() == expected_word.lower(), (
                    f"Mismatch at {cid} order {order}: glossary={g['word']} vs dict={expected_word}"
                )
                g["entryId"] = expected_entries[order - 1]["id"]
                g["sourceRowIndex"] = expected_entries[order - 1]["rowIndex"]
                assert f"**{g['surface']}**" in en_full, (
                    f"Surface form **{g['surface']}** for {g['word']} not bolded in {art['id']}"
                )
            plain_full = en_full.replace("**", "")
            for s in art["sentences"]:
                assert s["sentence"] in plain_full, f"Sentence note not found verbatim in {art['id']}: {s['sentence']}"

        assert set(covered_orders.keys()) == set(range(1, total_day_words + 1)), (
            f"Incomplete coverage in {cid}: {set(range(1, total_day_words + 1)) - set(covered_orders.keys())}"
        )

        day_folder = DESKTOP_ARTICLE_DIR / f"{chap['group']}第{chap['groupDay']}天"
        day_folder.mkdir(parents=True, exist_ok=True)
        for art in arts:
            md_text = render_clean_article_markdown(art)
            md_path = day_folder / f"英语文章{art['articleNumber']}.md"
            md_path.write_text(md_text, encoding="utf-8")
            art["sourcePath"] = str(md_path).replace("\\", "/")

    if wc_errors:
        for err in wc_errors:
            print("ERROR:", err)
        raise AssertionError("\n".join(wc_errors))

    # Write updated 阅读目录.md
    index_lines = [
        f"# 23考研英语词汇闪过 · 每日英语阅读目录（前{len(by_chap)}天 / {len(ARTICLES_SPEC)}篇）",
        "",
        "| 学习日 | 章节ID | 计划日期 | 当日词量 | 文章1 | 文章2 |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for cid, arts in by_chap.items():
        chap = chap_map[cid]
        total_w = chap["end"] - chap["start"]
        a1, a2 = arts[0], arts[1]
        folder_name = f"{chap['group']}第{chap['groupDay']}天"
        index_lines.append(
            f"| {folder_name}（{a1['wordList']}） | `{cid}` | {a1['scheduledDate']} | {total_w}词 "
            f"| [{a1['title']}（{a1['wordCount']}词）]({folder_name}/英语文章1.md) "
            f"| [{a2['title']}（{a2['wordCount']}词）]({folder_name}/英语文章2.md) |"
        )
    (DESKTOP_ARTICLE_DIR / "阅读目录.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    # Clean all 104 articles in C:\Users\hp\Desktop\每日英语文章
    cet6_dir = pathlib.Path(r"C:\Users\hp\Desktop\每日英语文章")
    cet6_files = [f for f in sorted(cet6_dir.rglob("英语文章*.md")) if "旧版" not in str(f)]
    for f in cet6_files:
        clean_existing_markdown_file(f)
    print(f"Cleaned boilerplate from {len(cet6_files)} CET-6 reading markdown files.")

    ARTICLES_JSON_OUT.write_text(json.dumps(ARTICLES_SPEC, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {ARTICLES_JSON_OUT} and {DESKTOP_ARTICLE_DIR}")


if __name__ == "__main__":
    main()
