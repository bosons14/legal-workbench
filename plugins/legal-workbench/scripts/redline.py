#!/usr/bin/env python3
"""Compare two versions of a document and produce a redline.

Works on anything extract_text.py can read (.docx, .pdf, .txt, .md, .html).
Paragraphs are aligned first, then changed paragraphs get a word-level diff.

Usage:
    redline.py OLD NEW [-f md|html] [-o OUT] [--changes-only]

Markdown output marks deletions as ~~struck~~ and insertions as **bold**.
HTML output uses <del>/<ins> with red/blue styling and opens in any browser
(and can be pasted into Word).
"""
import argparse
import difflib
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_text import paragraphs  # noqa: E402

TOKEN = re.compile(r"\s+|[^\s\w]|\w+")


def word_diff(a, b, fmt):
    ta, tb = TOKEN.findall(a), TOKEN.findall(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        old, new = "".join(ta[i1:i2]), "".join(tb[j1:j2])
        if op == "equal":
            out.append(html.escape(old) if fmt == "html" else old)
            continue
        if fmt == "html":
            if op in ("delete", "replace") and old:
                out.append(f"<del>{html.escape(old)}</del>")
            if op in ("insert", "replace") and new:
                out.append(f"<ins>{html.escape(new)}</ins>")
            continue
        # markdown: keep surrounding whitespace outside the markers
        src = old if old.strip() else new
        lead = src[:len(src) - len(src.lstrip())]
        tail_src = new if new.strip() else old
        trail = tail_src[len(tail_src.rstrip()):]
        parts = []
        if op in ("delete", "replace") and old.strip():
            parts.append(f"~~{old.strip()}~~")
        if op in ("insert", "replace") and new.strip():
            parts.append(f"**{new.strip()}**")
        out.append(lead + " ".join(parts) + trail if parts else old + new)
    return "".join(out)


def redline(old_paras, new_paras, fmt="md", changes_only=False):
    sm = difflib.SequenceMatcher(None, old_paras, new_paras, autojunk=False)
    blocks, stats = [], {"inserted": 0, "deleted": 0, "modified": 0, "unchanged": 0}

    def wrap(kind, body, ref):
        if fmt == "html":
            return f'<p class="{kind}"><span class="ref">{ref}</span> {body}</p>'
        label = {"ins": "[ADDED]", "del": "[DELETED]", "mod": "[CHANGED]", "eq": ""}[kind]
        return f"{ref} {label} {body}".replace("  ", " ").strip()

    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            stats["unchanged"] += i2 - i1
            if not changes_only:
                for k in range(i1, i2):
                    body = html.escape(old_paras[k]) if fmt == "html" else old_paras[k]
                    blocks.append(wrap("eq", body, f"N{j1 + k - i1 + 1}"))
            continue
        olds, news = old_paras[i1:i2], new_paras[j1:j2]
        # pair up similar paragraphs inside a replace block
        pairs = []
        if op == "replace":
            used = set()
            for oi, o in enumerate(olds):
                best, best_r = None, 0.45
                for ni, n in enumerate(news):
                    if ni in used:
                        continue
                    r = difflib.SequenceMatcher(None, o, n).ratio()
                    if r > best_r:
                        best, best_r = ni, r
                if best is not None:
                    used.add(best)
                    pairs.append((oi, best))
            paired_o = {p[0] for p in pairs}
            paired_n = {p[1] for p in pairs}
        else:
            paired_o, paired_n = set(), set()
        for oi, o in enumerate(olds):
            if oi not in paired_o:
                stats["deleted"] += 1
                body = f"<del>{html.escape(o)}</del>" if fmt == "html" else f"~~{o}~~"
                blocks.append(wrap("del", body, f"O{i1 + oi + 1}"))
        for oi, ni in sorted(pairs, key=lambda p: p[1]):
            stats["modified"] += 1
            blocks.append(wrap("mod", word_diff(olds[oi], news[ni], fmt), f"N{j1 + ni + 1}"))
        for ni, n in enumerate(news):
            if ni not in paired_n:
                stats["inserted"] += 1
                body = f"<ins>{html.escape(n)}</ins>" if fmt == "html" else f"**{n}**"
                blocks.append(wrap("ins", body, f"N{j1 + ni + 1}"))
    return blocks, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("-f", "--format", choices=["md", "html"], default="md")
    ap.add_argument("-o", "--out")
    ap.add_argument("--changes-only", action="store_true", help="omit unchanged paragraphs")
    a = ap.parse_args()

    blocks, stats = redline(paragraphs(a.old), paragraphs(a.new), a.format, a.changes_only)
    summary = (f"{stats['modified']} paragraph(s) changed, {stats['inserted']} added, "
               f"{stats['deleted']} deleted, {stats['unchanged']} unchanged")
    if a.format == "html":
        doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Redline</title>
<style>body{{font-family:Georgia,serif;max-width:52rem;margin:2rem auto;line-height:1.55;padding:0 1rem}}
del{{color:#b3261e;text-decoration:line-through}} ins{{color:#0b57d0;text-decoration:underline}}
p.ins{{border-left:3px solid #0b57d0;padding-left:.6rem}} p.del{{border-left:3px solid #b3261e;padding-left:.6rem}}
p.mod{{border-left:3px solid #e8a200;padding-left:.6rem}} .ref{{color:#888;font:12px monospace}}</style></head>
<body><h1>Redline</h1><p><b>Old:</b> {html.escape(a.old)}<br><b>New:</b> {html.escape(a.new)}<br>{summary}</p><hr>
{chr(10).join(blocks)}</body></html>"""
    else:
        doc = (f"# Redline\n\n- Old: `{a.old}`\n- New: `{a.new}`\n- {summary}\n\n"
               "Legend: ~~deleted~~ **inserted**; refs O# = old paragraph, N# = new paragraph\n\n---\n\n"
               + "\n\n".join(blocks) + "\n")
    if a.out:
        Path(a.out).write_text(doc, encoding="utf-8")
        print(f"{summary}\nwrote {a.out}", file=sys.stderr)
    else:
        sys.stdout.write(doc)


if __name__ == "__main__":
    main()
