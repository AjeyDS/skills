#!/usr/bin/env python3
"""Measure each .page block of the talk-track HTML against the printable page height.

Guessing whether text fits wastes render cycles; this reports the overflow per page in
inches so you can tune font-size / line-height / prose by a known amount.

It renders the HTML in headless Chrome at the printable *width* and reads each
`.page` element's height. The defaults match assets/template.html (US Letter,
margins 0.42in top / 0.5in sides / 0.38in bottom -> 7.5in wide, 10.2in tall).

Usage:
    python3 measure.py talk-track.html [--width-in 7.5] [--avail-in 10.2]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from find_chrome import find_chrome  # noqa: E402

PROBE = """<script>
window.addEventListener('load', () => {
  const IN = n => +(n / 96).toFixed(3);
  const pages = [...document.querySelectorAll('.page')].map((p, i) => ({
    id: p.id || ('page' + (i + 1)),
    height_in: IN(p.getBoundingClientRect().height),
  }));
  document.title = 'MEASURE' + JSON.stringify(pages) + 'END';
});
</script></body>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--width-in", type=float, default=7.5)
    ap.add_argument("--avail-in", type=float, default=10.2)
    a = ap.parse_args()

    src = open(a.html, encoding="utf-8").read()
    if "</body>" not in src:
        raise SystemExit("HTML has no </body> tag to hook the probe onto.")
    if ".page" not in src and 'class="page' not in src:
        raise SystemExit("No .page elements found — wrap each page in <div class=\"page\">.")

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     dir=os.path.dirname(os.path.abspath(a.html)),
                                     encoding="utf-8") as fh:
        fh.write(src.replace("</body>", PROBE))
        probe_path = fh.name
    try:
        out = subprocess.run(
            [find_chrome(), "--headless=new", "--disable-gpu",
             f"--window-size={int(a.width_in * 96)},1400",
             "--virtual-time-budget=3000", "--dump-dom", probe_path],
            capture_output=True, text=True,
        ).stdout
    finally:
        os.unlink(probe_path)

    m = re.search(r"MEASURE(\[.*?\])END", out)
    if not m:
        raise SystemExit("Probe did not report — Chrome may have failed to render the file.")
    pages = json.loads(m.group(1))
    print(f"printable: {a.width_in}in wide x {a.avail_in}in tall")
    worst = 0.0
    for p in pages:
        over = p["height_in"] - a.avail_in
        worst = max(worst, over)
        flag = "OVER" if over > 0 else ("tight" if over > -0.15 else "ok")
        print(f"  {p['id']:<8} {p['height_in']:6.2f}in   {over:+.2f}in  {flag}")
    if worst > 0:
        print(f"\n{worst:.2f}in over on the worst page. Tighten by at least that much.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
