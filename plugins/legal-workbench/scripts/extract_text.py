#!/usr/bin/env python3
"""Extract plain text from legal documents (.docx, .pdf, .txt, .md, .html, .rtf-lite).

Standard library only, except PDFs, which use `pdftotext` (poppler) if installed.

Usage:
    extract_text.py FILE [-o OUT] [--numbered]

--numbered prefixes every paragraph with [P<n>] so later analysis (review
comments, chronologies, citations) can point back to exact paragraphs.
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _docx_paragraphs(path):
    with zipfile.ZipFile(path) as z:
        parts = ["word/document.xml"]
        parts += sorted(n for n in z.namelist() if re.match(r"word/(footnotes|endnotes)\.xml$", n))
        out = []
        for part in parts:
            if part not in z.namelist():
                continue
            root = ET.fromstring(z.read(part))
            for p in root.iter(W + "p"):
                buf = []
                for node in p.iter():
                    tag = node.tag
                    if tag == W + "t" and node.text:
                        # skip text inside deletions (w:del contains w:delText, not w:t)
                        buf.append(node.text)
                    elif tag == W + "tab":
                        buf.append("\t")
                    elif tag in (W + "br", W + "cr"):
                        buf.append("\n")
                text = "".join(buf).strip()
                if text:
                    out.append(text)
        return out


def _pdf_text(path):
    if not shutil.which("pdftotext"):
        sys.exit("pdftotext not found - install poppler-utils (apt/brew install poppler) to read PDFs.")
    res = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"pdftotext failed: {res.stderr.strip()}")
    text = res.stdout
    if len(text.strip()) < 20:
        print("warning: almost no text extracted - this PDF may be scanned; OCR it first "
              "(e.g. `ocrmypdf in.pdf out.pdf`).", file=sys.stderr)
    return text


def _html_text(raw):
    raw = re.sub(r"(?is)<(script|style).*?</\1>", "", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>|</li>", "\n", raw)
    return html.unescape(re.sub(r"<[^>]+>", "", raw))


def paragraphs(path):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".docx":
        return _docx_paragraphs(path)
    if ext == ".pdf":
        text = _pdf_text(path)
    else:
        text = path.read_text(encoding="utf-8", errors="replace")
        if ext in (".html", ".htm"):
            text = _html_text(text)
        elif ext == ".rtf":
            text = re.sub(r"\\[a-z]+-?\d* ?|[{}]", "", text)
    paras = [re.sub(r"[ \t]+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    return [p for p in paras if p]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("-o", "--out")
    ap.add_argument("--numbered", action="store_true", help="prefix paragraphs with [P1], [P2], ...")
    a = ap.parse_args()
    paras = paragraphs(a.file)
    if a.numbered:
        paras = [f"[P{i}] {p}" for i, p in enumerate(paras, 1)]
    text = "\n\n".join(paras) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {len(paras)} paragraphs to {a.out}", file=sys.stderr)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
