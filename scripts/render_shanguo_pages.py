"""Render the scanned source once so parallel OCR does not contend on the 673 MB PDF."""

from __future__ import annotations

import argparse
from pathlib import Path

import pypdfium2 as pdfium


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--start-page", type=int, required=True)
    parser.add_argument("--end-page", type=int, required=True)
    parser.add_argument("--scale", type=float, default=1.3)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    document = pdfium.PdfDocument(str(args.pdf), password="")
    for pdf_page in range(args.start_page, args.end_page + 1):
        output = args.output_dir / f"page-{pdf_page:04d}.jpg"
        if output.exists():
            continue
        image = document[pdf_page - 1].render(scale=args.scale).to_pil().convert("RGB")
        image.save(output, "JPEG", quality=92, optimize=True)
        if pdf_page % 10 == 0:
            print(f"Rendered page {pdf_page}/{args.end_page}", flush=True)


if __name__ == "__main__":
    main()
