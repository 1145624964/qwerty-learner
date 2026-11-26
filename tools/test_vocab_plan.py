from __future__ import annotations

import re
import unittest
from datetime import date, timedelta
from pathlib import Path


PLAN_PATH = Path(__file__).resolve().parents[1] / "六级词汇闪过每日学习计划.md"


def daily_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for line in PLAN_PATH.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\| 2026-\d{2}-\d{2} \|", line):
            rows.append([part.strip() for part in line.strip("|").split("|")])
    return rows


class ReviewScheduleTest(unittest.TestCase):
    def test_plan_includes_sixteen_dedicated_review_days(self) -> None:
        rows = daily_rows()
        review_rows = [row for row in rows if row[2].startswith("复习第")]

        self.assertEqual(108, len(rows))
        self.assertEqual(16, len(review_rows))

    def test_review_dates_follow_the_approved_cadence(self) -> None:
        review_dates = [row[0] for row in daily_rows() if row[2].startswith("复习第")]

        self.assertEqual(
            [
                "2026-09-14", "2026-09-15", "2026-09-22", "2026-09-29",
                "2026-10-06", "2026-10-13", "2026-10-20", "2026-10-27",
                "2026-11-01", "2026-11-08", "2026-11-15", "2026-11-22",
                "2026-11-29", "2026-12-06", "2026-12-13", "2026-12-18",
            ],
            review_dates,
        )

    def test_calendar_is_contiguous_and_ends_on_december_eighteenth(self) -> None:
        rows = daily_rows()
        actual = [date.fromisoformat(row[0]) for row in rows]
        expected = [date(2026, 9, 2) + timedelta(days=offset) for offset in range(108)]

        self.assertEqual(expected, actual)
        self.assertEqual("2026-12-18", rows[-1][0])

    def test_first_two_reviews_cover_the_already_studied_medium_words(self) -> None:
        rows_by_date = {row[0]: row for row in daily_rows()}

        self.assertEqual("复习第1天", rows_by_date["2026-09-14"][2])
        self.assertIn("中频词第1至6天", rows_by_date["2026-09-14"][3])
        self.assertIn("Word List 1至3", rows_by_date["2026-09-14"][3])
        self.assertEqual("复习第2天", rows_by_date["2026-09-15"][2])
        self.assertIn("中频词第7至12天", rows_by_date["2026-09-15"][3])
        self.assertIn("Word List 4至6", rows_by_date["2026-09-15"][3])

    def test_all_ninety_two_learning_tasks_remain_in_the_requested_order(self) -> None:
        study_rows = [row for row in daily_rows() if row[2].startswith("学习第")]
        tasks = [row[3] for row in study_rows]

        self.assertEqual(92, len(study_rows))
        self.assertTrue(all(task.startswith("中频词") for task in tasks[:24]))
        self.assertTrue(all(task.startswith("低频词") for task in tasks[24:52]))
        self.assertTrue(all(task.startswith("高频词") for task in tasks[52:70]))
        self.assertTrue(all(task.startswith("简单词") for task in tasks[70:]))
        self.assertEqual(5346, sum(int(row[4]) for row in study_rows))

    def test_october_fifth_is_today_and_low_frequency_day_six(self) -> None:
        today_rows = [row for row in daily_rows() if row[5] == "今天"]

        self.assertEqual(1, len(today_rows))
        self.assertEqual("2026-10-05", today_rows[0][0])
        self.assertEqual("学习第30天", today_rows[0][2])
        self.assertEqual("低频词 · 第6天", today_rows[0][3])


if __name__ == "__main__":
    unittest.main()
