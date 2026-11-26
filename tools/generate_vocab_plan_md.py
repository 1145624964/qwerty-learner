from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


OUTPUT = Path(__file__).resolve().parents[1] / "六级词汇闪过每日学习计划.md"
START_DATE = date(2026, 9, 2)
TODAY = date(2026, 10, 5)
WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

SECTIONS = [
    {
        "name": "中频词",
        "counts": [42, 42, 43, 42, 42, 42, 43, 42, 43, 42, 43, 42,
                   42, 42, 43, 42, 39, 39, 41, 40, 42, 42, 43, 42],
        "word_lists": True,
    },
    {
        "name": "低频词",
        "counts": [50] * 26 + [49, 49],
        "word_lists": False,
    },
    {
        "name": "高频词",
        "counts": [41, 41, 42, 41, 41, 41, 41, 41, 41, 41, 41, 40,
                   39, 38, 41, 40, 42, 41],
        "word_lists": True,
    },
    {
        "name": "简单词",
        "counts": [101] * 10 + [100] * 12,
        "word_lists": False,
    },
]


def study_task(section: dict[str, object], section_day: int) -> str:
    if section["word_lists"]:
        word_list = (section_day + 1) // 2
        return f"{section['name']} · Word List {word_list} · 第{section_day}天"
    return f"{section['name']} · 第{section_day}天"


def review_task(
    section: dict[str, object], start_day: int, end_day: int, final_review: bool
) -> str:
    name = str(section["name"])
    total_days = len(section["counts"])
    if final_review:
        if section["word_lists"]:
            total_lists = (total_days + 1) // 2
            return f"{name}综合复习 · Word List 1至{total_lists} · 整理全部错词"
        return f"{name}综合复习 · 第1至{total_days}天 · 整理全部错词"

    if section["word_lists"]:
        first_list = (start_day + 1) // 2
        last_list = (end_day + 1) // 2
        return (
            f"复习{name}第{start_day}至{end_day}天 · "
            f"Word List {first_list}至{last_list} · 回顾错词"
        )
    return f"复习{name}第{start_day}至{end_day}天 · 回顾错词"


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    current = START_DATE
    learning_day = 1
    review_day = 1

    def add_study(section: dict[str, object], section_day: int) -> None:
        nonlocal current, learning_day
        count = section["counts"][section_day - 1]
        rows.append(
            {
                "date": current,
                "weekday": WEEKDAYS[current.weekday()],
                "progress": f"学习第{learning_day}天",
                "task": study_task(section, section_day),
                "new_words": count,
                "status": "今天" if current == TODAY else "",
                "section": section["name"],
                "kind": "study",
            }
        )
        current += timedelta(days=1)
        learning_day += 1

    def add_review(
        section: dict[str, object], start_day: int, end_day: int, final_review: bool
    ) -> None:
        nonlocal current, review_day
        rows.append(
            {
                "date": current,
                "weekday": WEEKDAYS[current.weekday()],
                "progress": f"复习第{review_day}天",
                "task": review_task(section, start_day, end_day, final_review),
                "new_words": "—",
                "status": "今天" if current == TODAY else "",
                "section": section["name"],
                "kind": "review",
            }
        )
        current += timedelta(days=1)
        review_day += 1

    for index, section in enumerate(SECTIONS):
        total_days = len(section["counts"])

        if index == 0:
            # September 2-13 have already been completed without review days.
            for section_day in range(1, 13):
                add_study(section, section_day)
            add_review(section, 1, 6, final_review=False)
            add_review(section, 7, 12, final_review=False)
            next_day = 13
        else:
            next_day = 1

        while next_day <= total_days:
            chunk_end = min(next_day + 5, total_days)
            for section_day in range(next_day, chunk_end + 1):
                add_study(section, section_day)
            add_review(
                section,
                next_day,
                chunk_end,
                final_review=chunk_end == total_days,
            )
            next_day = chunk_end + 1

    return rows


def build_markdown(rows: list[dict[str, object]]) -> str:
    today_row = next(row for row in rows if row["date"] == TODAY)
    section_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        section_rows[str(row["section"])].append(row)

    lines = [
        "# 六级词汇闪过每日学习计划",
        "",
        "本计划从2026年9月2日开始，包含92个新词学习日和16个专门复习日，共108天。学习顺序为中频词、低频词、高频词、简单词；原有学习章节和词量全部保留。",
        "",
        f"**今日进度：** {TODAY.isoformat()}　{today_row['progress']}　{today_row['task']}　{today_row['new_words']}词",
        "",
        "**近期安排：** 10月5日为学习第30天，学习低频词第6天；10月6日为复习第5天，复习低频词第1至6天；10月7日从低频词第7天继续学习新词。",
        "",
        "## 计划概览",
        "",
        "| 栏目 | 学习日 | 复习日 | 日期范围 | 词条量 | 每日新词 |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]

    for section in SECTIONS:
        name = str(section["name"])
        grouped = section_rows[name]
        study_count = sum(row["kind"] == "study" for row in grouped)
        review_count = sum(row["kind"] == "review" for row in grouped)
        counts = section["counts"]
        lines.append(
            f"| {name} | {study_count}天 | {review_count}天 | "
            f"{grouped[0]['date'].isoformat()} 至 {grouped[-1]['date'].isoformat()} | "
            f"{sum(counts)}词 | {min(counts)}至{max(counts)}词 |"
        )

    lines.extend(
        [
            f"| 合计 | 92天 | 16天 | {rows[0]['date'].isoformat()} 至 {rows[-1]['date'].isoformat()} | 5346词 | — |",
            "",
            "## 复习规则",
            "",
            "- 9月14日和9月15日用于补上已经完成的前12个中频词学习日的复习。",
            "- 此后每完成6个新词学习日，安排1个不学习新词的复习日。栏目最后不足6天时，完成剩余内容后仍安排1个复习日。",
            "- 普通复习日重点复习最近一组学习内容，并重新测试此前记录的错词。",
            "- 每个词汇栏目结束后的复习日为综合复习，覆盖该栏目的全部内容和累计错词。",
            "",
            "## 每日安排",
        ]
    )

    by_month: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        day = row["date"]
        by_month[(day.year, day.month)].append(row)

    for (year, month), month_rows in by_month.items():
        lines.extend(
            [
                "",
                f"### {year}年{month}月",
                "",
                "| 日期 | 星期 | 计划进度 | 学习或复习内容 | 新词数 | 状态 |",
                "| --- | --- | --- | --- | ---: | --- |",
            ]
        )
        for row in month_rows:
            lines.append(
                f"| {row['date'].isoformat()} | {row['weekday']} | {row['progress']} | "
                f"{row['task']} | {row['new_words']} | {row['status']} |"
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    rows = build_rows()
    OUTPUT.write_text(build_markdown(rows), encoding="utf-8", newline="\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
