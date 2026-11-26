from __future__ import annotations

import hashlib
import json
import pathlib
import re
from collections import Counter, defaultdict
from datetime import date, timedelta
from typing import Any

MD_ROOT = pathlib.Path(r"C:\Users\hp\Desktop\23考研英语词汇闪过_Markdown")
CHUNKS_DIR = MD_ROOT / "分册"
REPO_ROOT = pathlib.Path(r"C:\Users\hp\Documents\qwerty-learner")
DICTS_DIR = REPO_ROOT / "public" / "dicts"
RESOURCES_DIR = REPO_ROOT / "src" / "resources"

START_DATE = date(2026, 11, 19)
WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

HEADWORD_CORRECTIONS: dict[tuple[str, int, str], tuple[str, str]] = {
    ("24_偶考词_03_PDF390-395.md", 315, "delegater"): ("delegate", "2"),
    ("24_偶考词_04_PDF396-401.md", 111, "recta ngle"): ("rectangle", ""),
    ("24_偶考词_04_PDF396-401.md", 161, "OX"): ("ox", ""),
    ("24_偶考词_04_PDF396-401.md", 179, "coW"): ("cow", ""),
    ("25_简单词_01_PDF416-421.md", 203, "sOW"): ("sow", ""),
    ("25_简单词_06_PDF446-451.md", 93, "outsider"): ("outside", "1"),
    ("25_简单词_06_PDF446-451.md", 361, "ZOO"): ("zoo", ""),
    ("25_简单词_09_PDF464-469.md", 417, "rebel?"): ("rebel", "2"),
    ("25_简单词_11_PDF476-481.md", 159, "SO"): ("so", ""),
}


def load_reference_phonetics() -> dict[str, list[dict[str, Any]]]:
    ref_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
    priority_files = [
        "KaoYanShanGuo_2023.json",
        "shanguo_cet6_book_order.json",
        "KaoYan_2024.json",
        "KaoYan_3_T.json",
        "2025KaoYanHongBaoShu.json",
        "CET6_T.json",
        "CET4_T.json",
    ]
    for fname in priority_files:
        fpath = DICTS_DIR / fname
        if not fpath.exists():
            continue
        try:
            data = json.loads(fpath.read_text("utf-8"))
            for item in data:
                if isinstance(item, dict) and "name" in item:
                    w = item["name"].strip().lower()
                    ref_map[w].append(
                        {
                            "source": fname,
                            "usphone": (item.get("usphone") or "").strip(),
                            "ukphone": (item.get("ukphone") or "").strip(),
                            "trans": item.get("trans") or [],
                        }
                    )
        except Exception:
            pass
    return ref_map


def clean_headword(file_name: str, line_no: int, raw_token: str) -> tuple[str, str]:
    token = re.sub(r"^(?:〔OCR待核〕)?\*\*|\*\*$", "", raw_token).strip()
    token = re.sub(r"\[[^\]]+\]$", "", token).strip()
    if (file_name, line_no, token) in HEADWORD_CORRECTIONS:
        return HEADWORD_CORRECTIONS[(file_name, line_no, token)]

    m = re.match(r"^(.+?)([\'¹²³12\?]+)$", token)
    if m and token.lower() != "o'clock":
        base = m.group(1).strip()
        suf = m.group(2)
        h_idx = "1" if suf in ("'", "¹", "1") else ("2" if suf in ("²", "2", "?") else suf)
        return base, h_idx
    return token, ""


def extract_ocr_phonetic_and_def(rest_text: str) -> tuple[str, str, bool]:
    ocr_pending = "〔OCR待核〕" in rest_text
    s = rest_text.replace("〔OCR待核〕", " ").strip()
    parts = [p.strip() for p in s.split("|") if p.strip()]
    joined = " ".join(parts)

    m = re.match(r"^\[([^\]]+)\]\s*(.*)$", joined)
    if m:
        first_bracket = m.group(1).strip()
        if not re.match(r"^(?:C|U|sing\.?|pl\.?|the~|常用|亦用)", first_bracket):
            raw_phone = first_bracket
            defn = m.group(2).strip()
            return raw_phone, defn, ocr_pending

    return "", joined, ocr_pending


def parse_all_chunks(ref_map: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[tuple[str, int]]]:
    files = sorted(CHUNKS_DIR.glob("*.md"))
    entries: list[dict[str, Any]] = []
    index_items: list[tuple[str, int]] = []

    bold_re = re.compile(r"^(?:〔OCR待核〕)?\*\*([A-Za-z0-9\-\'\s/¹²³\.]+?)\*\*\s*\|(.*)$")
    cur_entry: dict[str, Any] | None = None

    for f in files:
        num = int(f.name.split("_")[0])
        lines = f.read_text("utf-8").splitlines()

        if num == 27:
            for line in lines:
                s = line.strip()
                if not s or s.startswith("#") or s.startswith(">"):
                    continue
                for part in s.split("|"):
                    p = part.strip()
                    m = re.match(r"^([A-Za-z0-9\-\'\s\.]+?)/(\d+)$", p)
                    if m:
                        index_items.append((m.group(1).strip(), int(m.group(2))))
                    elif p == "instinct67":
                        index_items.append(("instinct", 67))
            continue

        if num < 2 or num > 26:
            continue

        name_parts = f.name.split("_")
        section_group = name_parts[1]
        word_list = name_parts[2] if num <= 23 else None

        cur_pdf_page = None
        cur_book_page = None
        cur_theme = None
        cur_subtheme = None
        if num > 23:
            cur_entry = None

        for i, raw_line in enumerate(lines, 1):
            s = raw_line.strip()
            if not s or s.startswith(">") or s.startswith("原PDF页码："):
                continue

            if s.startswith("# "):
                continue

            if s.startswith("## PDF第"):
                pm = re.search(r"PDF第(\d+)页(?:（书内页(\d+)）)?", s)
                if pm:
                    cur_pdf_page = int(pm.group(1))
                    cur_book_page = int(pm.group(2)) if pm.group(2) else (cur_pdf_page - 11)
                continue

            if num <= 23:
                m = bold_re.match(s)
                if m:
                    raw_hw = m.group(1).strip()
                    rest = m.group(2).strip()
                    lemma, h_idx = clean_headword(f.name, i, raw_hw)
                    ocr_phone, defn, ocr_pending = extract_ocr_phonetic_and_def(rest)
                    if "〔OCR待核〕" in s:
                        ocr_pending = True

                    cur_entry = {
                        "rowIndex": len(entries),
                        "id": f"ky23-{len(entries):04d}",
                        "name": lemma,
                        "rawHeadword": raw_hw,
                        "homographIndex": h_idx,
                        "group": section_group,
                        "wordList": word_list,
                        "theme": None,
                        "subtheme": None,
                        "pdfPage": cur_pdf_page,
                        "bookPage": cur_book_page,
                        "sourceFile": f.name,
                        "sourceLine": i,
                        "ocrPhonetic": ocr_phone,
                        "ocrDefinition": defn,
                        "ocrPending": ocr_pending,
                        "mnemonic": "",
                        "phrases": [],
                        "extensions": [],
                    }
                    entries.append(cur_entry)
                elif cur_entry is not None:
                    if "|" in s and all(
                        re.match(r"^[A-Za-z\-\'\s]+$", part.strip()) for part in s.split("|") if part.strip()
                    ):
                        continue
                    clean_s = s.replace("〔OCR待核〕", "").strip()
                    if "〔OCR待核〕" in s:
                        cur_entry["ocrPending"] = True

                    if clean_s.startswith("记 |") or clean_s.startswith("记 ") or (
                        not cur_entry["mnemonic"]
                        and not cur_entry["phrases"]
                        and ("→" in clean_s or "一→" in clean_s or "本身为词根" in clean_s)
                        and "|" not in clean_s
                    ):
                        memo = re.sub(r"^记\s*\|?\s*", "", clean_s).strip()
                        cur_entry["mnemonic"] = memo
                    elif clean_s.startswith("用 |") or clean_s.startswith("用 "):
                        phr_part = re.sub(r"^用\s*\|?\s*", "", clean_s).strip()
                        for p in phr_part.split("|"):
                            if p.strip():
                                cur_entry["phrases"].append(p.strip())
                    elif re.match(r"^(?:扩|护|扒|折|办)\s*\|", clean_s) or clean_s.startswith("[派]") or clean_s.startswith("[近]") or clean_s.startswith("[反]"):
                        ext_part = re.sub(r"^(?:扩|护|扒|折|办)\s*\|\s*", "", clean_s).strip()
                        for p in ext_part.split("|"):
                            if p.strip():
                                cur_entry["extensions"].append(p.strip())
                    elif "|" in clean_s and any(
                        tag in clean_s for tag in ["[派]", "[近]", "[反]"]
                    ):
                        for p in clean_s.split("|"):
                            if p.strip():
                                cur_entry["extensions"].append(p.strip())
                    elif "|" in clean_s:
                        first_seg = clean_s.split("|")[0].strip()
                        if re.search(r"[A-Za-z]{2,}\s+.*[\u4e00-\u9fff]", first_seg) and not any(
                            k in first_seg for k in ["后缀", "词根", "Word List", "高频词", "中频词", "低频词"]
                        ):
                            for p in clean_s.split("|"):
                                if p.strip():
                                    cur_entry["phrases"].append(p.strip())
            else:
                if "|" not in s:
                    if s in ("偶考词", "简单词", "补充词") or len(s) == 1:
                        continue
                    if s in ("与人相关", "日常生活", "社会政经", "物体描述", "自然科学", "文体教育", "其他"):
                        cur_theme = s
                        cur_subtheme = None
                    else:
                        cur_subtheme = s
                    continue

                first_col, rest = s.split("|", 1)
                first_col = first_col.strip()
                rest = rest.strip()

                inline_phone = ""
                m_inline = re.match(r"^([A-Za-z]+)\[([^\]]+)\]$", first_col)
                if m_inline:
                    raw_hw = m_inline.group(1)
                    inline_phone = m_inline.group(2)
                else:
                    raw_hw = first_col

                lemma, h_idx = clean_headword(f.name, i, raw_hw)
                ocr_phone, defn, ocr_pending = extract_ocr_phonetic_and_def(rest)
                if inline_phone and not ocr_phone:
                    ocr_phone = inline_phone
                if "〔OCR待核〕" in s:
                    ocr_pending = True

                entries.append(
                    {
                        "rowIndex": len(entries),
                        "id": f"ky23-{len(entries):04d}",
                        "name": lemma,
                        "rawHeadword": raw_hw,
                        "homographIndex": h_idx,
                        "group": section_group,
                        "wordList": None,
                        "theme": cur_theme,
                        "subtheme": cur_subtheme,
                        "pdfPage": cur_pdf_page,
                        "bookPage": cur_book_page,
                        "sourceFile": f.name,
                        "sourceLine": i,
                        "ocrPhonetic": ocr_phone,
                        "ocrDefinition": defn,
                        "ocrPending": ocr_pending,
                        "mnemonic": "",
                        "phrases": [],
                        "extensions": [],
                    }
                )

    for entry in entries:
        w_lower = entry["name"].lower()
        refs = ref_map.get(w_lower, [])
        usphone = ""
        ukphone = ""
        phonetic_source = "ocr"
        for r in refs:
            if r["usphone"] or r["ukphone"]:
                usphone = r["usphone"] or r["ukphone"]
                ukphone = r["ukphone"] or r["usphone"]
                phonetic_source = r["source"]
                break
        if not usphone and entry["ocrPhonetic"]:
            usphone = entry["ocrPhonetic"]
            ukphone = entry["ocrPhonetic"]

        defn = re.sub(r"\s+", " ", entry["ocrDefinition"]).strip()

        # Build notation for Qwerty Learner (mnemonic + top phrases)
        notation_parts = []
        if entry["mnemonic"]:
            notation_parts.append(f"【记】{entry['mnemonic']}")
        if entry["phrases"]:
            clean_phrases = [re.sub(r"[团圆图国園]$", "[真]", p) for p in entry["phrases"][:4]]
            notation_parts.append(f"【用】{' ｜ '.join(clean_phrases)}")
        if entry["extensions"]:
            notation_parts.append(f"【扩】{' ｜ '.join(entry['extensions'][:2])}")

        entry["usphone"] = usphone
        entry["ukphone"] = ukphone
        entry["phoneticSource"] = phonetic_source
        entry["trans"] = [defn] if defn else []
        entry["notation"] = "  ".join(notation_parts) if notation_parts else ""

    return entries, index_items


def build_chapters(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []

    # 1. Frequency words: High (WL 01-10), Medium (WL 11-14), Low (WL 15-22)
    # Split each WordList into 2 daily chapters
    wl_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in entries:
        if e["wordList"]:
            wl_groups[e["wordList"]].append(e)

    group_day_counter: dict[str, int] = defaultdict(int)
    group_prefix_map = {
        "高频词": "ky23-high",
        "中频词": "ky23-medium",
        "低频词": "ky23-low",
        "偶考词": "ky23-rare",
        "简单词": "ky23-simple",
        "补充词": "ky23-supp",
    }

    for wl_num in range(1, 23):
        wl_key = f"WordList{wl_num:02d}"
        wl_items = wl_groups[wl_key]
        group_name = wl_items[0]["group"]
        prefix = group_prefix_map[group_name]
        total = len(wl_items)
        split_idx = (total + 1) // 2
        part1 = wl_items[:split_idx]
        part2 = wl_items[split_idx:]

        for part_no, part_items in enumerate([part1, part2], 1):
            group_day_counter[group_name] += 1
            g_day = group_day_counter[group_name]
            start_idx = part_items[0]["rowIndex"]
            end_idx = part_items[-1]["rowIndex"] + 1
            chapters.append(
                {
                    "id": f"{prefix}-wl{wl_num:02d}-day-{g_day}",
                    "group": group_name,
                    "wordList": f"Word List {wl_num}",
                    "groupDay": g_day,
                    "name": f"Word List {wl_num} · 第{g_day}天",
                    "start": start_idx,
                    "end": end_idx,
                }
            )

    # 2. Non-WordList sections: 偶考词 (24 days), 简单词 (22 days), 补充词 (8 days)
    non_wl_configs = [
        ("偶考词", 24),
        ("简单词", 22),
        ("补充词", 8),
    ]
    for group_name, num_days in non_wl_configs:
        sec_items = [e for e in entries if e["group"] == group_name]
        total = len(sec_items)
        base_size = total // num_days
        remainder = total % num_days
        prefix = group_prefix_map[group_name]
        offset = 0
        for d in range(1, num_days + 1):
            count = base_size + (1 if d <= remainder else 0)
            part_items = sec_items[offset : offset + count]
            offset += count
            start_idx = part_items[0]["rowIndex"]
            end_idx = part_items[-1]["rowIndex"] + 1
            chapters.append(
                {
                    "id": f"{prefix}-day-{d}",
                    "group": group_name,
                    "wordList": None,
                    "groupDay": d,
                    "name": f"第{d}天",
                    "start": start_idx,
                    "end": end_idx,
                }
            )

    return chapters


def build_study_plan(chapters: list[dict[str, Any]]) -> dict[str, Any]:
    """Build daily study & review schedule in original book order (High -> Medium -> Low -> Rare -> Simple -> Supp)."""
    section_order = ["高频词", "中频词", "低频词", "偶考词", "简单词", "补充词"]
    tasks: list[dict[str, Any]] = []
    current_date = START_DATE
    learning_day = 1
    review_day = 1

    for sec_name in section_order:
        sec_chaps = [c for c in chapters if c["group"] == sec_name]
        total_sec_days = len(sec_chaps)
        batch_chaps: list[dict[str, Any]] = []

        for idx, chap in enumerate(sec_chaps, 1):
            word_count = chap["end"] - chap["start"]
            task_label = f"{sec_name} · {chap['name']}"
            tasks.append(
                {
                    "id": f"plan-study-{learning_day:03d}",
                    "scheduledDate": current_date.isoformat(),
                    "weekday": WEEKDAYS[current_date.weekday()],
                    "kind": "study",
                    "learningDay": learning_day,
                    "reviewDay": None,
                    "progressLabel": f"学习第{learning_day}天",
                    "section": sec_name,
                    "sectionDay": idx,
                    "chapterId": chap["id"],
                    "reviewChapterIds": [],
                    "taskLabel": task_label,
                    "newWords": word_count,
                }
            )
            current_date += timedelta(days=1)
            learning_day += 1
            batch_chaps.append(chap)

            is_last_in_sec = idx == total_sec_days
            if len(batch_chaps) == 6 or is_last_in_sec:
                start_d = batch_chaps[0]["groupDay"]
                end_d = batch_chaps[-1]["groupDay"]
                if not is_last_in_sec:
                    if batch_chaps[0]["wordList"]:
                        wl_first = batch_chaps[0]["wordList"]
                        wl_last = batch_chaps[-1]["wordList"].replace("Word List ", "")
                        r_label = f"复习{sec_name}第{start_d}至{end_d}天 · {wl_first}至{wl_last} · 回顾错词"
                    else:
                        r_label = f"复习{sec_name}第{start_d}至{end_d}天 · 回顾错词"
                    tasks.append(
                        {
                            "id": f"plan-review-{review_day:03d}",
                            "scheduledDate": current_date.isoformat(),
                            "weekday": WEEKDAYS[current_date.weekday()],
                            "kind": "review",
                            "learningDay": None,
                            "reviewDay": review_day,
                            "progressLabel": f"复习第{review_day}天",
                            "section": sec_name,
                            "sectionDay": None,
                            "chapterId": None,
                            "reviewChapterIds": [c["id"] for c in batch_chaps],
                            "taskLabel": r_label,
                            "newWords": 0,
                        }
                    )
                    current_date += timedelta(days=1)
                    review_day += 1
                else:
                    # If the last batch has < 6 days or == 6 days, we do comprehensive section review
                    if batch_chaps[0]["wordList"]:
                        wl_first = sec_chaps[0]["wordList"]
                        wl_last = sec_chaps[-1]["wordList"].replace("Word List ", "")
                        r_label = f"{sec_name}综合复习 · {wl_first}至{wl_last} · 整理全部错词"
                    else:
                        r_label = f"{sec_name}综合复习 · 第1至{total_sec_days}天 · 整理全部错词"
                    tasks.append(
                        {
                            "id": f"plan-review-{review_day:03d}",
                            "scheduledDate": current_date.isoformat(),
                            "weekday": WEEKDAYS[current_date.weekday()],
                            "kind": "review",
                            "learningDay": None,
                            "reviewDay": review_day,
                            "progressLabel": f"复习第{review_day}天",
                            "section": sec_name,
                            "sectionDay": None,
                            "chapterId": None,
                            "reviewChapterIds": [c["id"] for c in sec_chaps],
                            "taskLabel": r_label,
                            "newWords": 0,
                        }
                    )
                    current_date += timedelta(days=1)
                    review_day += 1
                batch_chaps = []

    return {
        "id": "kaoyan-shanguo-2023-plan-v1",
        "title": "23考研英语词汇闪过每日学习计划",
        "dictionaryId": "kaoyan-shanguo-2023-book-order",
        "targetExam": "考研全国英语一",
        "timezone": "Asia/Shanghai",
        "startDate": START_DATE.isoformat(),
        "endDate": (current_date - timedelta(days=1)).isoformat(),
        "totalStudyDays": learning_day - 1,
        "totalReviewDays": review_day - 1,
        "totalDays": len(tasks),
        "totalEntries": sum(c["end"] - c["start"] for c in chapters),
        "groupOrder": section_order,
        "tasks": tasks,
    }


def write_plan_markdown(plan: dict[str, Any], chapters: list[dict[str, Any]]) -> str:
    tasks = plan["tasks"]
    lines: list[str] = [
        "# 23考研英语词汇闪过每日学习计划",
        "",
        f"本计划从 {plan['startDate']} 开始，按原书顺序（高频词 → 中频词 → 低频词 → 偶考词 → 简单词 → 补充词）编排，"
        f"包含 {plan['totalStudyDays']} 个新词学习日和 {plan['totalReviewDays']} 个专门复习日，共 {plan['totalDays']} 天，覆盖全书 {plan['totalEntries']} 个词条。",
        "",
        "## 计划概览",
        "",
        "| 栏目 | 学习日 | 复习日 | 日期范围 | 词条量 | 每日新词 |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]

    for sec in plan["groupOrder"]:
        sec_tasks = [t for t in tasks if t["section"] == sec]
        study_t = [t for t in sec_tasks if t["kind"] == "study"]
        rev_t = [t for t in sec_tasks if t["kind"] == "review"]
        counts = [t["newWords"] for t in study_t]
        min_c, max_c = min(counts), max(counts)
        c_range = f"{min_c}词" if min_c == max_c else f"{min_c}至{max_c}词"
        lines.append(
            f"| {sec} | {len(study_t)}天 | {len(rev_t)}天 | {sec_tasks[0]['scheduledDate']} 至 {sec_tasks[-1]['scheduledDate']} | {sum(counts)}词 | {c_range} |"
        )

    lines.extend(
        [
            f"| 合计 | {plan['totalStudyDays']}天 | {plan['totalReviewDays']}天 | {plan['startDate']} 至 {plan['endDate']} | {plan['totalEntries']}词 | — |",
            "",
            "## 复习规则",
            "",
            "- 每完成 6 个新词学习日，安排 1 个不学习新词的专门复习日；每个词汇栏目结束时安排 1 个该栏目综合复习日。",
            "- 频考词（高频 20 天、中频 8 天、低频 16 天，共 44 个学习日）按纸书 Word List 1—22 拆分，每个 Word List 分 2 天学习，每天配套两篇考研英语一风格强化阅读。",
            "- 学习进度由实际完成记录驱动，日历日期仅作计划排期参考，不自动将过期或今日任务标为已完成。",
            "",
            "## 每日安排",
        ]
    )

    by_month: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for t in tasks:
        d = date.fromisoformat(t["scheduledDate"])
        by_month[(d.year, d.month)].append(t)

    for (yr, mo), m_tasks in by_month.items():
        lines.extend(
            [
                "",
                f"### {yr}年{mo}月",
                "",
                "| 日期 | 星期 | 计划进度 | 学习或复习内容 | 新词数 |",
                "| --- | --- | --- | --- | ---: |",
            ]
        )
        for t in m_tasks:
            nw = str(t["newWords"]) if t["kind"] == "study" else "—"
            lines.append(
                f"| {t['scheduledDate']} | {t['weekday']} | {t['progressLabel']} | {t['taskLabel']} | {nw} |"
            )

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ref_map = load_reference_phonetics()
    entries, index_items = parse_all_chunks(ref_map)
    chapters = build_chapters(entries)
    plan = build_study_plan(chapters)

    # 1. Write public/dicts/shanguo_kaoyan_2023_book_order.json (Qwerty Learner compatible + rich metadata)
    dict_out = DICTS_DIR / "shanguo_kaoyan_2023_book_order.json"
    dict_out.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 2. Write src/resources/shanguo_kaoyan_2023_chapters.json
    chap_out = RESOURCES_DIR / "shanguo_kaoyan_2023_chapters.json"
    chap_out.write_text(json.dumps(chapters, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 3. Write src/resources/shanguo_kaoyan_2023_plan.json
    plan_out = RESOURCES_DIR / "shanguo_kaoyan_2023_plan.json"
    plan_out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 4. Write Desktop & Repo Markdown study plan
    plan_md = write_plan_markdown(plan, chapters)
    (REPO_ROOT / "23考研英语词汇闪过每日学习计划.md").write_text(plan_md, encoding="utf-8")
    (pathlib.Path(r"C:\Users\hp\Desktop\23考研英语词汇闪过每日学习计划.md")).write_text(plan_md, encoding="utf-8")

    print(f"Wrote {len(entries)} entries to {dict_out}")
    print(f"Wrote {len(chapters)} chapters to {chap_out}")
    print(f"Wrote {plan['totalDays']} plan tasks ({plan['totalStudyDays']} study + {plan['totalReviewDays']} review) to {plan_out}")


if __name__ == "__main__":
    main()
