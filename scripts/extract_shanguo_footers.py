"""OCR the high-frequency page footers used as an independent order check."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / ".tools" / "rapidocr"))

import cv2  # noqa: E402
from rapidocr_onnxruntime import RapidOCR  # noqa: E402


def main() -> None:
    image_dir = REPO_ROOT / "tmp" / "pdfs" / "rendered"
    output = REPO_ROOT / "tmp" / "pdfs" / "ocr-high-footers.json"
    engine = RapidOCR(intra_op_num_threads=4, inter_op_num_threads=1)
    pages = []
    for pdf_page in range(13, 168):
        image = cv2.imread(str(image_dir / f"page-{pdf_page:04d}.jpg"), cv2.IMREAD_COLOR)
        top = int(image.shape[0] * 0.88)
        observations, _ = engine(image[top:, :], use_cls=False)
        pages.append(
            {
                "pdf_page": pdf_page,
                "book_page": pdf_page - 12,
                "items": [
                    {"text": text, "confidence": float(confidence), "left": float(min(point[0] for point in box))}
                    for box, text, confidence in observations or []
                ],
            }
        )
        if pdf_page % 20 == 0:
            output.write_text(json.dumps({"pages": pages}, ensure_ascii=False), encoding="utf-8")
            print(f"Footer OCR page {pdf_page}/167", flush=True)
    output.write_text(json.dumps({"pages": pages}, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
