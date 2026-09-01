"""Extract OCR observations from the scanned 六级词汇闪过 PDF.

The source PDF is image-only. This script renders the requested PDF pages,
runs RapidOCR locally, and stores text boxes plus basic colour statistics for
later headword classification and manual verification.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAPIDOCR_PATH = REPO_ROOT / ".tools" / "rapidocr"
sys.path.insert(0, str(RAPIDOCR_PATH))

import cv2  # noqa: E402
import numpy as np  # noqa: E402
import pypdfium2 as pdfium  # noqa: E402
from rapidocr_onnxruntime import RapidOCR  # noqa: E402


ASCII_TEXT = re.compile(r"^[A-Za-z][A-Za-z0-9 '\-.,]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--start-page", type=int, required=True, help="First PDF page, one-based")
    parser.add_argument("--end-page", type=int, required=True, help="Last PDF page, one-based and inclusive")
    parser.add_argument("--scale", type=float, default=2.0)
    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Read pre-rendered page-NNNN.jpg images instead of rendering the PDF",
    )
    parser.add_argument(
        "--crop-ratio",
        type=float,
        default=0.45,
        help="OCR only the left part containing headwords",
    )
    parser.add_argument(
        "--ocr-threads",
        type=int,
        default=4,
        help="ONNX threads per model; bounded to avoid oversubscribing large CPUs",
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=10,
        help="Persist partial OCR output after this many pages",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from pages already stored in the output file",
    )
    return parser.parse_args()


def box_colour_stats(hsv_image: np.ndarray, box: list[list[float]]) -> dict[str, float]:
    xs = [int(point[0]) for point in box]
    ys = [int(point[1]) for point in box]
    left = max(0, min(xs) - 3)
    right = min(hsv_image.shape[1], max(xs) + 4)
    top = max(0, min(ys) - 3)
    bottom = min(hsv_image.shape[0], max(ys) + 4)
    crop = hsv_image[top:bottom, left:right]
    if crop.size == 0:
        return {"hue": 0.0, "saturation": 0.0, "value": 0.0}
    return {
        "hue": round(float(crop[:, :, 0].mean()), 2),
        "saturation": round(float(crop[:, :, 1].mean()), 2),
        "value": round(float(crop[:, :, 2].mean()), 2),
    }


def main() -> None:
    args = parse_args()
    if not RAPIDOCR_PATH.exists():
        raise SystemExit(f"RapidOCR dependency not found: {RAPIDOCR_PATH}")

    document = None if args.image_dir else pdfium.PdfDocument(str(args.pdf), password="")
    page_count = 475 if document is None else len(document)
    if args.start_page < 1 or args.end_page > page_count or args.start_page > args.end_page:
        raise SystemExit(f"Invalid page range for {page_count}-page PDF")

    engine = RapidOCR(
        intra_op_num_threads=args.ocr_threads,
        inter_op_num_threads=1,
    )
    pages: list[dict[str, object]] = []
    completed_pages: set[int] = set()
    if args.resume and args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if float(existing.get("scale", 0)) != args.scale:
            raise SystemExit("Cannot resume OCR generated with a different render scale")
        pages = existing.get("pages", [])
        completed_pages = {int(page["pdf_page"]) for page in pages}

    def write_checkpoint() -> None:
        pages.sort(key=lambda page: int(page["pdf_page"]))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps({"scale": args.scale, "pages": pages}, ensure_ascii=False),
            encoding="utf-8",
        )

    for pdf_page in range(args.start_page, args.end_page + 1):
        if pdf_page in completed_pages:
            print(f"Skip completed page {pdf_page}/{args.end_page}", flush=True)
            continue
        if args.image_dir:
            image_path = args.image_dir / f"page-{pdf_page:04d}.jpg"
            if not image_path.exists():
                raise SystemExit(f"Pre-rendered page not found: {image_path}")
            bgr_image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
            if bgr_image is None:
                raise SystemExit(f"Unable to read pre-rendered page: {image_path}")
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        else:
            assert document is not None
            rgb_image = np.array(document[pdf_page - 1].render(scale=args.scale).to_pil().convert("RGB"))
        source_width = int(rgb_image.shape[1])
        ocr_width = max(1, int(source_width * args.crop_ratio))
        rgb_image = rgb_image[:, :ocr_width]
        hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
        observations, elapsed = engine(rgb_image, use_cls=False)

        items = []
        for box, text, confidence in observations or []:
            rounded_box = [[round(float(x), 2), round(float(y), 2)] for x, y in box]
            xs = [point[0] for point in rounded_box]
            ys = [point[1] for point in rounded_box]
            items.append(
                {
                    "text": text,
                    "confidence": round(float(confidence), 4),
                    "box": rounded_box,
                    "left": min(xs),
                    "top": min(ys),
                    "width": max(xs) - min(xs),
                    "height": max(ys) - min(ys),
                    "ascii_only": bool(ASCII_TEXT.fullmatch(text)),
                    **box_colour_stats(hsv_image, box),
                }
            )

        pages.append(
            {
                "pdf_page": pdf_page,
                "book_page": pdf_page - 12,
                "image_width": source_width,
                "image_height": int(rgb_image.shape[0]),
                "elapsed": elapsed,
                "items": items,
            }
        )
        print(f"OCR page {pdf_page}/{args.end_page}: {len(items)} observations", flush=True)
        if len(pages) % args.checkpoint_every == 0:
            write_checkpoint()
            print(f"Checkpointed {len(pages)} pages to {args.output}", flush=True)

    write_checkpoint()
    print(f"Wrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
