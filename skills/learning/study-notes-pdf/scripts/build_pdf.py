#!/usr/bin/env python3
"""
Build a styled study-notes PDF from a Markdown file.

    python3 build_pdf.py notes.md --out "Topic — Study Notes.pdf" [--title T] [--subtitle S] [--html-only]

What it does
  1. Markdown -> HTML (python-markdown; tables, fenced code, attr_list, toc).
  2. Callout blockquotes:  "> **Mental model:** ..." / Example / Remember / Gotcha / Interview answer / Exam tip
     become coloured boxes.
  3. ```mermaid fences are rendered by mermaid.js inside the printing browser. A local copy of
     mermaid.min.js is inlined (found in node_modules, or fetched once into ~/.cache with npm);
     the CDN is the last resort.
  4. Local SVG images are inlined so they print crisp; other images are embedded as data URIs so the
     PDF never depends on a relative path.
  5. Cover page + table of contents (skip with --no-toc) + automatic section numbering (do not number
     headings yourself) + page footer.
  6. HTML -> PDF with headless Chromium via Playwright (Python or Node), falling back to wkhtmltopdf.

Exit code is non-zero with a clear message if no renderer is available.
"""
import argparse
import base64
import datetime as dt
import html
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import markdown  # type: ignore
except ImportError:  # pragma: no cover
    sys.exit("python-markdown is required:  pip install markdown --break-system-packages")

HERE = Path(__file__).resolve().parent
CSS_PATH = HERE.parent / "assets" / "study.css"

CALLOUTS = {
    "mental model": "model",
    "model": "model",
    "analogy": "model",
    "example": "example",
    "worked example": "example",
    "remember": "remember",
    "key point": "remember",
    "takeaway": "remember",
    "gotcha": "gotcha",
    "warning": "gotcha",
    "trap": "gotcha",
    "interview answer": "interview",
    "interview": "interview",
    "exam tip": "exam",
    "exam": "exam",
}

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"


# ---------------------------------------------------------------- mermaid
def find_mermaid_js() -> str | None:
    """Locate a local mermaid.min.js; fetch one into a cache with npm if none is found."""
    cache = Path.home() / ".cache" / "study-notes-pdf" / "mermaid.min.js"
    candidates = [
        HERE.parent / "assets" / "mermaid.min.js",
        cache,
    ]
    for root in (Path.home() / ".npm-global" / "lib" / "node_modules", Path("/usr/local/lib/node_modules"),
                 Path("/usr/lib/node_modules"), Path.cwd() / "node_modules"):
        candidates += [root / "mermaid" / "dist" / "mermaid.min.js",
                       root / "@mermaid-js" / "mermaid-cli" / "node_modules" / "mermaid" / "dist" / "mermaid.min.js"]
    for c in candidates:
        if c.exists() and c.stat().st_size > 100_000:
            return c.read_text(encoding="utf-8")
    npm = shutil.which("npm")
    if npm:
        tmp = Path(tempfile.mkdtemp(prefix="mermaid_dl_"))
        try:
            r = subprocess.run([npm, "pack", "mermaid@11", "--silent"], cwd=tmp, capture_output=True, text=True, timeout=180)
            tgz = next(tmp.glob("mermaid-*.tgz"), None)
            if r.returncode == 0 and tgz:
                subprocess.run(["tar", "-xzf", str(tgz), "package/dist/mermaid.min.js"], cwd=tmp, check=True)
                src = tmp / "package" / "dist" / "mermaid.min.js"
                cache.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, cache)
                return cache.read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[build_pdf] could not download mermaid: {e}\n")
    return None


def render_mermaid_blocks(md_text: str, workdir: Path) -> tuple[str, bool]:
    """Replace ```mermaid fences with <pre class="mermaid"> rendered in the browser at print time."""
    found = [False]

    def repl(m: re.Match) -> str:
        found[0] = True
        code = m.group(1).strip()
        return f'\n<div class="diagram" markdown="0"><pre class="mermaid">{html.escape(code)}</pre></div>\n'

    new = re.sub(r"```mermaid\s*\n(.*?)```", repl, md_text, flags=re.S)
    return new, found[0]


# ---------------------------------------------------------------- images
def embed_images(html_text: str, base: Path) -> str:
    def repl(m: re.Match) -> str:
        tag = m.group(0)
        src = m.group(1)
        if src.startswith(("http://", "https://", "data:")):
            return tag
        p = (base / src).resolve()
        if not p.exists():
            sys.stderr.write(f"[build_pdf] WARNING image not found: {src}\n")
            return tag
        if p.suffix.lower() == ".svg":
            svg = p.read_text(encoding="utf-8", errors="ignore")
            svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
            return f'<div class="diagram">{svg}</div>'
        mime = mimetypes.guess_type(str(p))[0] or "image/png"
        data = base64.b64encode(p.read_bytes()).decode()
        tag = tag.replace(src, f"data:{mime};base64,{data}")
        if 'class="' not in tag:
            tag = tag.replace("<img", '<img class="figure"', 1)
        return tag

    return re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', repl, html_text)


# ---------------------------------------------------------------- callouts
def style_callouts(html_text: str) -> str:
    """<blockquote><p><strong>Label:</strong> text -> <blockquote class="callout-x"><span class=label>"""
    pat = re.compile(r"<blockquote>\s*<p>\s*<strong>([^<]{2,40}?):?</strong>:?\s*", re.S)

    def repl(m: re.Match) -> str:
        label = m.group(1).strip().rstrip(":")
        kind = CALLOUTS.get(label.lower())
        if not kind:
            return m.group(0)
        return f'<blockquote class="callout-{kind}"><span class="label">{html.escape(label)}</span><p>'

    return pat.sub(repl, html_text)


def style_captions(html_text: str) -> str:
    # a paragraph that is entirely italic directly after a figure/diagram/img becomes a caption
    return re.sub(r"(</div>|/>|</figure>)\s*<p><em>(.*?)</em></p>", r'\1<p class="caption">\2</p>', html_text, flags=re.S)


# ---------------------------------------------------------------- toc / numbering
def number_and_toc(html_text: str) -> tuple[str, str]:
    h2 = 0
    h3 = 0
    items = []

    def repl(m: re.Match) -> str:
        nonlocal h2, h3
        level = m.group(1)
        attrs = m.group(2) or ""
        text = m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        anchor = idm.group(1) if idm else re.sub(r"[^a-z0-9]+", "-", re.sub("<[^>]+>", "", text).lower()).strip("-")
        if level == "2":
            h2 += 1
            h3 = 0
            num = f"{h2}"
            items.append(("2", num, re.sub("<[^>]+>", "", text), anchor))
        else:
            h3 += 1
            num = f"{h2}.{h3}"
            items.append(("3", num, re.sub("<[^>]+>", "", text), anchor))
        attrs2 = attrs if idm else attrs + f' id="{anchor}"'
        return f'<h{level}{attrs2}><span class="num">{num}</span>{text}</h{level}>'

    out = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", repl, html_text, flags=re.S)
    toc = ['<div class="toc"><h2>Contents</h2><ol>']
    for level, num, text, anchor in items:
        cls = ' class="lvl3"' if level == "3" else ""
        toc.append(f'<li{cls}><a href="#{anchor}">{num}&nbsp;&nbsp;{html.escape(html.unescape(text))}</a></li>')
    toc.append("</ol></div>")
    return out, "\n".join(toc)


# ---------------------------------------------------------------- page assembly
def build_html(md_path: Path, title: str | None, subtitle: str | None, workdir: Path, no_toc: bool = False) -> tuple[str, bool]:
    text = md_path.read_text(encoding="utf-8")

    # title from first H1
    m = re.search(r"^# (.+)$", text, flags=re.M)
    if m:
        title = title or m.group(1).strip()
        text = text[: m.start()] + text[m.end():]
    title = title or md_path.stem

    text, browser_mermaid = render_mermaid_blocks(text, workdir)
    # python-markdown merges blockquotes separated only by a blank line; keep callouts separate
    text = re.sub(r"(^>.*\n)\n+(?=>)", r"\1\n<div class=\"bq-sep\"></div>\n\n", text, flags=re.M)

    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "attr_list", "md_in_html", "sane_lists", "toc", "smarty"],
        extension_configs={"toc": {"permalink": False}},
        output_format="html5",
    )
    body = style_callouts(body)
    body = embed_images(body, md_path.parent)
    body = style_captions(body)
    body, toc = number_and_toc(body)

    css = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.exists() else ""
    today = dt.date.today().strftime("%B %d, %Y")
    cover = f"""
<section class="cover">
  <div class="eyebrow">Study notes</div>
  <h1>{html.escape(title)}</h1>
  {f'<div class="subtitle">{html.escape(subtitle)}</div>' if subtitle else ''}
  <div class="meta">{today}</div>
  <div class="howto">
    <strong>How to read this.</strong> Sections go from the big picture down to the details.
    Stop at any section and you still have a coherent picture; keep going for the mechanism.
    Coloured boxes are the parts to re-read: <em>mental models</em>, <em>examples</em>, and <em>remember</em> lines.
  </div>
</section>
"""
    mermaid_script = ""
    if browser_mermaid:
        local_js = find_mermaid_js()
        loader = f"<script>{local_js}</script>" if local_js else f'<script src="{MERMAID_CDN}"></script>'
        if not local_js:
            sys.stderr.write("[build_pdf] WARNING: no local mermaid.js found; using CDN (needs network in the browser)\n")
        mermaid_script = f"""
{loader}
<script>
  mermaid.initialize({{ startOnLoad: false, theme: 'neutral', themeVariables: {{ fontSize: '16px' }}, flowchart: {{ useMaxWidth: true, htmlLabels: true }}, sequence: {{ useMaxWidth: true }} }});
  window.__mermaidDone = false;
  mermaid.run({{ querySelector: '.mermaid' }}).then(() => {{ window.__mermaidDone = true; }})
    .catch(e => {{ console.error(e); window.__mermaidDone = true; }});
</script>"""
    doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{css}</style></head>
<body>
{cover}
{'' if no_toc else toc}
<main>
{body}
</main>
{mermaid_script}
</body></html>"""
    return doc, browser_mermaid


# ---------------------------------------------------------------- renderers
def render_with_playwright_py(html_path: Path, pdf_path: Path, title: str, wait_mermaid: bool) -> bool:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return False
    footer = (
        '<div style="font-size:8pt;color:#5b6b7a;width:100%;padding:0 16mm;display:flex;'
        'justify-content:space-between;font-family:system-ui,sans-serif">'
        f"<span>{html.escape(title)}</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>"
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        if wait_mermaid:
            try:
                page.wait_for_function("window.__mermaidDone === true", timeout=60000)
            except Exception:  # noqa: BLE001
                sys.stderr.write("[build_pdf] WARNING: mermaid did not finish rendering in time\n")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_path),
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=footer,
            margin={"top": "18mm", "bottom": "20mm", "left": "16mm", "right": "16mm"},
            prefer_css_page_size=False,
        )
        browser.close()
    return True


def render_with_playwright_node(html_path: Path, pdf_path: Path, title: str, wait_mermaid: bool) -> bool:
    if not shutil.which("node"):
        return False
    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch({{ args: ['--no-sandbox'] }});
  const p = await b.newPage();
  await p.goto({html_path.as_uri()!r}, {{ waitUntil: 'networkidle' }});
  if ({str(wait_mermaid).lower()}) {{ try {{ await p.waitForFunction('window.__mermaidDone === true', {{ timeout: 60000 }}); }} catch (e) {{}} }}
  await p.emulateMedia({{ media: 'print' }});
  await p.pdf({{ path: {str(pdf_path)!r}, format: 'Letter', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="font-size:8pt;color:#5b6b7a;width:100%;padding:0 16mm;display:flex;justify-content:space-between;font-family:system-ui,sans-serif"><span>{html.escape(title)}</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>`,
    margin: {{ top: '18mm', bottom: '20mm', left: '16mm', right: '16mm' }} }});
  await b.close();
}})().catch(e => {{ console.error(e); process.exit(1); }});
"""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(script)
        js = f.name
    r = subprocess.run(["node", js], capture_output=True, text=True)
    os.unlink(js)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-600:])
        return False
    return True


def render_with_wkhtmltopdf(html_path: Path, pdf_path: Path, title: str) -> bool:
    exe = shutil.which("wkhtmltopdf")
    if not exe:
        return False
    cmd = [exe, "--quiet", "--enable-local-file-access", "--page-size", "Letter",
           "--margin-top", "18mm", "--margin-bottom", "20mm", "--margin-left", "16mm", "--margin-right", "16mm",
           "--footer-left", title, "--footer-right", "[page] / [topage]", "--footer-font-size", "8",
           "--javascript-delay", "3000", str(html_path), str(pdf_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0 and pdf_path.exists()


def page_count(pdf_path: Path) -> int | None:
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True)
        m = re.search(r"Pages:\s+(\d+)", r.stdout)
        if m:
            return int(m.group(1))
    try:
        from pypdf import PdfReader  # type: ignore
        return len(PdfReader(str(pdf_path)).pages)
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown", help="notes.md")
    ap.add_argument("--out", "-o", help="output PDF path (default: <stem>.pdf)")
    ap.add_argument("--title")
    ap.add_argument("--subtitle")
    ap.add_argument("--html-only", action="store_true", help="write the HTML next to the PDF path and stop")
    ap.add_argument("--no-toc", action="store_true", help="skip the contents page (use for short docs, under ~8 body pages)")
    args = ap.parse_args()

    md_path = Path(args.markdown).resolve()
    if not md_path.exists():
        sys.exit(f"not found: {md_path}")
    pdf_path = Path(args.out).resolve() if args.out else md_path.with_suffix(".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    workdir = Path(tempfile.mkdtemp(prefix="study_notes_"))
    doc, browser_mermaid = build_html(md_path, args.title, args.subtitle, workdir, no_toc=args.no_toc)
    html_path = pdf_path.with_suffix(".html")
    html_path.write_text(doc, encoding="utf-8")
    title = args.title or (re.search(r"<title>(.*?)</title>", doc).group(1) if "<title>" in doc else md_path.stem)
    title = html.unescape(title)
    if args.html_only:
        print(f"HTML written: {html_path}")
        return

    ok = (render_with_playwright_py(html_path, pdf_path, title, browser_mermaid)
          or render_with_playwright_node(html_path, pdf_path, title, browser_mermaid)
          or render_with_wkhtmltopdf(html_path, pdf_path, title))
    if not ok:
        sys.exit("No PDF renderer available. Install one of:\n"
                 "  pip install playwright --break-system-packages && playwright install chromium\n"
                 "  npm i -g playwright && npx playwright install chromium\n"
                 "  apt-get install wkhtmltopdf")
    n = page_count(pdf_path)
    print(f"PDF written: {pdf_path}" + (f"  ({n} pages)" if n else ""))
    if browser_mermaid:
        print("note: contains mermaid diagrams — render a page to PNG and check they are legible.")


if __name__ == "__main__":
    main()
