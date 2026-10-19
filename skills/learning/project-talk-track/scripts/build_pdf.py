#!/usr/bin/env python3
"""Render the talk-track HTML to PDF with headless Chrome and verify the page count.

Also writes one PNG per page (if pypdfium2 is installed) so you can *look* at the
layout — wrapped labels, misaligned bands and bad glyph fallbacks only show up visually.

Usage:
    python3 build_pdf.py talk-track.html [--out talk-track.pdf] [--expect-pages 3] [--png-dir previews]
Exit code 1 if the page count does not match --expect-pages.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from find_chrome import find_chrome  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", default=None)
    ap.add_argument("--expect-pages", type=int, default=3)
    ap.add_argument("--png-dir", default=None, help="write page-N.png previews here")
    ap.add_argument("--scale", type=float, default=1.6, help="PNG render scale")
    a = ap.parse_args()

    html = os.path.abspath(a.html)
    out = os.path.abspath(a.out or os.path.splitext(html)[0] + ".pdf")
    subprocess.run(
        [find_chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={out}", html],
        capture_output=True, text=True,
    )
    if not os.path.exists(out):
        raise SystemExit("Chrome produced no PDF.")

    try:
        from pypdf import PdfReader
    except ImportError:
        raise SystemExit("pip install pypdf  (needed to verify the page count)")
    n = len(PdfReader(out).pages)
    print(f"wrote {out}  ({os.path.getsize(out) // 1024} KB, {n} page{'s' if n != 1 else ''})")

    if a.png_dir:
        try:
            import pypdfium2 as pdfium
        except ImportError:
            print("pypdfium2 not installed — skipping PNG previews (pip install pypdfium2)")
        else:
            os.makedirs(a.png_dir, exist_ok=True)
            doc = pdfium.PdfDocument(out)
            for i in range(len(doc)):
                p = os.path.join(a.png_dir, f"page-{i + 1}.png")
                doc[i].render(scale=a.scale).to_pil().save(p)
                print(f"  preview: {p}")

    if n != a.expect_pages:
        print(f"\nEXPECTED {a.expect_pages} pages, got {n}. "
              f"Run measure.py to see which page overflows, then tighten.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
