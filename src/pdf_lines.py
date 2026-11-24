"""Rebuild visual text lines from PDF word positions (robust to column-ordered text streams)."""
import pdfplumber
def page_lines(page, x_tol=6, y_tol=2.5):
    words = page.extract_words(x_tolerance=x_tol, y_tolerance=y_tol, keep_blank_chars=False, use_text_flow=False)
    words.sort(key=lambda w: (round(w["top"]), w["x0"]))
    lines, cur, top = [], [], None
    for w in words:
        if top is None or abs(w["top"] - top) <= y_tol: cur.append(w); top = w["top"] if top is None else top
        else: lines.append(cur); cur, top = [w], w["top"]
    if cur: lines.append(cur)
    return [" ".join(x["text"] for x in sorted(l, key=lambda w: w["x0"])) for l in lines]
def pdf_lines(path, **kw):
    with pdfplumber.open(path) as pdf:
        return [(i + 1, ln) for i, pg in enumerate(pdf.pages) for ln in page_lines(pg, **kw)]
