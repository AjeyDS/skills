#!/usr/bin/env python3
"""
Download an image for the study notes and validate that it is actually a usable diagram.

    python3 fetch_image.py <url> <out-path> [--min-width 400] [--referer URL]

Exit 0 and print the saved path on success. Exit 1 with a one-line reason on failure
(blocked, not an image, too small, looks like a logo/avatar) — treat failure as "draw it instead".
"""
import argparse
import io
import sys
import urllib.request
import urllib.error

try:
    from PIL import Image  # type: ignore
except ImportError:
    Image = None  # validated on size only

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("out")
    ap.add_argument("--min-width", type=int, default=400)
    ap.add_argument("--referer", default=None)
    ap.add_argument("--max-bytes", type=int, default=8 * 1024 * 1024)
    a = ap.parse_args()

    headers = {"User-Agent": UA, "Accept": "image/avif,image/webp,image/svg+xml,image/*,*/*;q=0.8"}
    if a.referer:
        headers["Referer"] = a.referer
    req = urllib.request.Request(a.url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            data = r.read(a.max_bytes + 1)
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code} from {a.url}")
    except Exception as e:  # noqa: BLE001
        fail(f"could not fetch: {e}")

    if len(data) > a.max_bytes:
        fail("image larger than max size")
    if len(data) < 8 * 1024 and not ctype.endswith("svg+xml"):
        fail(f"too small ({len(data)} bytes) — probably a placeholder or tracking pixel")
    if not ctype.startswith("image/"):
        head = data[:200].lower()
        if b"<svg" in head:
            ctype = "image/svg+xml"
        elif data[:8] == b"\x89PNG\r\n\x1a\n":
            ctype = "image/png"
        elif data[:3] == b"\xff\xd8\xff":
            ctype = "image/jpeg"
        else:
            fail(f"not an image (content-type {ctype or 'unknown'}) — likely an HTML page or a block")

    if ctype == "image/svg+xml":
        out = a.out if a.out.lower().endswith(".svg") else a.out.rsplit(".", 1)[0] + ".svg"
        with open(out, "wb") as f:
            f.write(data)
        print(out)
        return

    if Image is not None:
        try:
            im = Image.open(io.BytesIO(data))
            w, h = im.size
        except Exception as e:  # noqa: BLE001
            fail(f"could not decode image: {e}")
        if w < a.min_width:
            fail(f"too narrow ({w}px) — will not be legible on the page")
        if w < 600 and h < 600 and 0.8 <= w / max(h, 1) <= 1.25:
            fail(f"small near-square image ({w}x{h}) — looks like a logo or avatar")
        if im.mode in ("P", "RGBA") and a.out.lower().endswith((".jpg", ".jpeg")):
            im = im.convert("RGB")
            im.save(a.out, quality=90)
            print(a.out)
            return
    with open(a.out, "wb") as f:
        f.write(data)
    print(a.out)


if __name__ == "__main__":
    main()
