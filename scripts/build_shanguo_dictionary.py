"""Turn OCR observations into an ordered, book-aligned CET-6 dictionary.

This script deliberately separates OCR extraction from publication. It first
emits page-level candidates and diagnostics; only the fully validated 5,346
printed rows are allowed to become the application's dictionary.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
ASCII_WORD = re.compile(r"^[a-z][a-z '\-]*$")


@dataclass(frozen=True)
class ChapterSpec:
    id: str
    group: str
    name: str
    first_book_page: int
    last_book_page: int


CHAPTERS = [
    ChapterSpec("high-1", "高频词", "Word List 1", 1, 18),
    ChapterSpec("high-2", "高频词", "Word List 2", 19, 36),
    ChapterSpec("high-3", "高频词", "Word List 3", 37, 55),
    ChapterSpec("high-4", "高频词", "Word List 4", 56, 74),
    ChapterSpec("high-5", "高频词", "Word List 5", 75, 92),
    ChapterSpec("high-6", "高频词", "Word List 6", 93, 110),
    ChapterSpec("high-7", "高频词", "Word List 7", 111, 127),
    ChapterSpec("high-8", "高频词", "Word List 8", 128, 141),
    ChapterSpec("high-9", "高频词", "Word List 9", 142, 155),
    ChapterSpec("medium-1", "中频词", "Word List 1", 156, 171),
    ChapterSpec("medium-2", "中频词", "Word List 2", 172, 187),
    ChapterSpec("medium-3", "中频词", "Word List 3", 188, 202),
    ChapterSpec("medium-4", "中频词", "Word List 4", 203, 219),
    ChapterSpec("medium-5", "中频词", "Word List 5", 220, 235),
    ChapterSpec("medium-6", "中频词", "Word List 6", 236, 251),
    ChapterSpec("medium-7", "中频词", "Word List 7", 252, 267),
    ChapterSpec("medium-8", "中频词", "Word List 8", 268, 284),
    ChapterSpec("medium-9", "中频词", "Word List 9", 285, 297),
    ChapterSpec("medium-10", "中频词", "Word List 10", 298, 308),
    ChapterSpec("medium-11", "中频词", "Word List 11", 309, 320),
    ChapterSpec("medium-12", "中频词", "Word List 12", 321, 332),
    ChapterSpec("low", "低频词", "完整词表", 333, 379),
    ChapterSpec("basic", "简单词", "完整词表", 380, 451),
]

# The cover advertises normalized vocabulary counts. Publication intentionally
# follows the body one row at a time, preserving separately printed homographs.
EXPECTED_GROUP_COUNTS = {"高频词": 734, "中频词": 1005, "低频词": 1374, "简单词": 2182}
PRINTED_ROW_COUNTS = {"高频词": 733, "中频词": 1005, "低频词": 1398, "简单词": 2210}
MEDIUM_BOOK_TRANSLATIONS = REPO_ROOT / "scripts" / "shanguo_medium_book_translations.json"
PREFERRED_DICTIONARIES = [
    "xinghuoqiaoji_6.json",
    "CET6_T.json",
    "DanCiDeJianFa_6.json",
    "2025KaoYanHongBaoShu.json",
    "coca20000.json",
]
MANUAL_ENTRIES = {
    "baby boom": {
        "name": "baby boom",
        "trans": ["n. 婴儿潮"],
        "usphone": "ˈbeɪbi buːm",
        "ukphone": "ˈbeɪbi buːm",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr-dir", type=Path, default=REPO_ROOT / "tmp" / "pdfs")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "tmp" / "pdfs" / "shanguo-candidates.json")
    parser.add_argument("--overrides", type=Path, default=REPO_ROOT / "scripts" / "shanguo_page_overrides.json")
    parser.add_argument("--publish", action="store_true", help="Write validated application dictionary and chapter JSON")
    parser.add_argument(
        "--dictionary-output",
        type=Path,
        default=REPO_ROOT / "public" / "dicts" / "shanguo_cet6_book_order.json",
    )
    parser.add_argument(
        "--chapters-output",
        type=Path,
        default=REPO_ROOT / "src" / "resources" / "shanguo_cet6_chapters.json",
    )
    return parser.parse_args()


def normalize_candidate(text: str) -> str:
    text = text.strip().lower().replace("’", "'").replace("‘", "'")
    text = re.sub(r"[\d¹²³⁴⁵⁶⁷⁸⁹⁰'.,]+$", "", text).strip()
    return re.sub(r"\s+", " ", text)


def load_lexicon() -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    entries: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in (REPO_ROOT / "public" / "dicts").glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            continue
        for word in data:
            if not isinstance(word, dict) or not isinstance(word.get("name"), str):
                continue
            name = normalize_candidate(word["name"])
            if ASCII_WORD.fullmatch(name):
                entries[name].append({"source": path.name, "word": word})
    return entries, sorted(entries)


def load_pages(ocr_dir: Path) -> dict[int, dict[str, Any]]:
    pages: dict[int, dict[str, Any]] = {}
    for filename in ["ocr-high.json", "ocr-medium.json", "ocr-low.json", "ocr-basic.json"]:
        path = ocr_dir / filename
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for page in data["pages"]:
            pages[int(page["book_page"])] = page
    return pages


def choose_dictionary_entry(name: str, lexicon: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    if name in MANUAL_ENTRIES:
        return MANUAL_ENTRIES[name]
    matches = lexicon.get(name, [])
    if not matches:
        raise SystemExit(f"No dictionary entry found for validated headword: {name}")

    priority = {source: index for index, source in enumerate(PREFERRED_DICTIONARIES)}

    def score(match: dict[str, Any]) -> tuple[int, int, int]:
        word = match["word"]
        translations = word.get("trans") if isinstance(word.get("trans"), list) else []
        phone_count = int(bool(word.get("usphone"))) + int(bool(word.get("ukphone")))
        return (priority.get(match["source"], len(priority)), -phone_count, -sum(len(str(item)) for item in translations))

    selected = min(matches, key=score)["word"]
    translations = selected.get("trans", [])
    if not isinstance(translations, list):
        translations = [str(translations)] if translations else []
    translations = [str(item) for item in translations if item is not None]
    return {
        "name": name,
        "trans": translations or ["书中词条"],
        "usphone": str(selected.get("usphone") or ""),
        "ukphone": str(selected.get("ukphone") or ""),
    }


def apply_medium_book_translations(dictionary: list[dict[str, Any]]) -> None:
    definitions = json.loads(MEDIUM_BOOK_TRANSLATIONS.read_text(encoding="utf-8"))
    medium_start = PRINTED_ROW_COUNTS["高频词"]
    medium_end = medium_start + PRINTED_ROW_COUNTS["中频词"]
    medium_words = dictionary[medium_start:medium_end]

    if len(definitions) != PRINTED_ROW_COUNTS["中频词"]:
        raise SystemExit(f"Expected 1005 medium-frequency book definitions, found {len(definitions)}")
    if [item.get("name") for item in definitions] != [word["name"] for word in medium_words]:
        raise SystemExit("Medium-frequency book definitions do not match the validated printed order")

    for word, definition in zip(medium_words, definitions, strict=True):
        translation = definition.get("trans")
        if not isinstance(translation, str) or not translation.strip():
            raise SystemExit(f"Missing medium-frequency book definition for {word['name']}")
        word["trans"] = [translation]


def extract_page_candidates(page: dict[str, Any]) -> list[dict[str, Any]]:
    max_left = float(page["image_width"]) * 0.34
    candidates = []
    for item in sorted(page["items"], key=lambda item: (item["top"], item["left"])):
        normalized = normalize_candidate(item["text"])
        if (
            float(item["saturation"]) >= 25
            and float(item["left"]) <= max_left
            and ASCII_WORD.fullmatch(normalized)
            and normalized.replace(" ", "") not in {"wordlist", "wordlimitt"}
            and not normalized.replace(" ", "").startswith("wordlist")
        ):
            candidates.append(
                {
                    "word": normalized,
                    "raw": item["text"],
                    "confidence": item["confidence"],
                    "top": item["top"],
                    "left": item["left"],
                }
            )
    return candidates


def main() -> None:
    args = parse_args()
    pages = load_pages(args.ocr_dir)
    lexicon, lexicon_words = load_lexicon()
    overrides = json.loads(args.overrides.read_text(encoding="utf-8")) if args.overrides.exists() else {}

    page_results: dict[str, list[dict[str, Any]]] = {}
    for book_page, page in sorted(pages.items()):
        candidates = extract_page_candidates(page)
        if str(book_page) in overrides:
            page_override = overrides[str(book_page)]
            if isinstance(page_override, list):
                candidates = [
                    {"word": word, "raw": "manual override", "confidence": 1.0, "top": index, "left": 0}
                    for index, word in enumerate(page_override)
                ]
            else:
                replacements = page_override.get("replace", {})
                for candidate in candidates:
                    if candidate["word"] in replacements:
                        candidate["word"] = replacements[candidate["word"]]
                        candidate["raw"] = "manual correction"
                        candidate["confidence"] = 1.0
                for insertion in page_override.get("insertAfter", []):
                    occurrence = int(insertion.get("occurrence", 1))
                    matching_indexes = [
                        index for index, candidate in enumerate(candidates) if candidate["word"] == insertion["after"]
                    ]
                    if len(matching_indexes) < occurrence:
                        raise SystemExit(f"Cannot apply insertion on book page {book_page}: {insertion}")
                    index = matching_indexes[occurrence - 1] + 1
                    candidates.insert(
                        index,
                        {
                            "word": insertion["word"],
                            "raw": "manual insertion",
                            "confidence": 1.0,
                            "top": candidates[index - 1]["top"] + 0.01,
                            "left": 0,
                        },
                    )
        for candidate in candidates:
            word = candidate["word"]
            candidate["in_lexicon"] = word in lexicon
            candidate["suggestions"] = [] if word in lexicon else difflib.get_close_matches(word, lexicon_words, n=5, cutoff=0.72)
        page_results[str(book_page)] = candidates

    chapter_results = []
    group_counts: dict[str, int] = defaultdict(int)
    offset = 0
    for chapter in CHAPTERS:
        words = [
            candidate
            for book_page in range(chapter.first_book_page, chapter.last_book_page + 1)
            for candidate in page_results.get(str(book_page), [])
        ]
        chapter_results.append(
            {
                "id": chapter.id,
                "group": chapter.group,
                "name": chapter.name,
                "firstBookPage": chapter.first_book_page,
                "lastBookPage": chapter.last_book_page,
                "start": offset,
                "end": offset + len(words),
                "count": len(words),
            }
        )
        offset += len(words)
        group_counts[chapter.group] += len(words)

    missing_pages = [page for page in range(1, 452) if page not in pages]
    diagnostics = {
        "processedPageCount": len(pages),
        "missingPages": missing_pages,
        "totalCandidates": sum(len(words) for words in page_results.values()),
        "groupCounts": dict(group_counts),
        "expectedGroupCounts": EXPECTED_GROUP_COUNTS,
        "groupCountMatches": {group: group_counts[group] == count for group, count in EXPECTED_GROUP_COUNTS.items()},
        "unknownCandidates": [
            {"bookPage": int(book_page), **candidate}
            for book_page, candidates in page_results.items()
            for candidate in candidates
            if not candidate["in_lexicon"]
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {"diagnostics": diagnostics, "chapters": chapter_results, "pages": page_results},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if args.publish:
        if missing_pages:
            raise SystemExit(f"Refusing to publish with {len(missing_pages)} unprocessed pages")
        if dict(group_counts) != PRINTED_ROW_COUNTS:
            raise SystemExit(f"Refusing to publish unexpected printed row counts: {dict(group_counts)}")

        ordered_candidates = [
            candidate
            for book_page in range(1, 452)
            for candidate in page_results[str(book_page)]
        ]
        dictionary = [choose_dictionary_entry(candidate["word"], lexicon) for candidate in ordered_candidates]
        if len(dictionary) != sum(PRINTED_ROW_COUNTS.values()):
            raise SystemExit("Published dictionary length does not match validated printed rows")
        apply_medium_book_translations(dictionary)

        published_chapters = [
            {
                "id": chapter["id"],
                "group": chapter["group"],
                "name": chapter["name"],
                "start": chapter["start"],
                "end": chapter["end"],
            }
            for chapter in chapter_results
        ]
        args.dictionary_output.parent.mkdir(parents=True, exist_ok=True)
        args.chapters_output.parent.mkdir(parents=True, exist_ok=True)
        args.dictionary_output.write_text(json.dumps(dictionary, ensure_ascii=False, indent=2), encoding="utf-8")
        args.chapters_output.write_text(json.dumps(published_chapters, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Published {len(dictionary)} ordered rows to {args.dictionary_output}")
        print(f"Published {len(published_chapters)} chapter boundaries to {args.chapters_output}")
    print(
        json.dumps(
            {
                "processedPageCount": diagnostics["processedPageCount"],
                "missingPageCount": len(missing_pages),
                "totalCandidates": diagnostics["totalCandidates"],
                "groupCounts": diagnostics["groupCounts"],
                "expectedGroupCounts": EXPECTED_GROUP_COUNTS,
                "groupCountMatches": diagnostics["groupCountMatches"],
                "unknownCandidateCount": len(diagnostics["unknownCandidates"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
