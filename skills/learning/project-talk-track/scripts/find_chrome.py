"""Locate a headless-capable Chrome/Chromium binary. Shared by measure.py and build_pdf.py."""
import os
import shutil

CANDIDATES = [
    os.environ.get("CHROME_BIN"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome"),
    shutil.which("google-chrome-stable"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
    shutil.which("chrome"),
]


def find_chrome():
    for c in CANDIDATES:
        if c and os.path.exists(c):
            return c
    raise SystemExit(
        "No Chrome/Chromium found. Install Google Chrome or set CHROME_BIN=/path/to/chrome."
    )
