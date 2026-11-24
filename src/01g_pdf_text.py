"""Dump text of a PDF (all pages) to data/interim/text/<name>.txt and print it. Usage: python -I src/01g_pdf_text.py <pdf> [maxchars]"""
import os, sys, pdfplumber
p = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
os.makedirs("data/interim/text", exist_ok=True)
with pdfplumber.open(p) as pdf:
    t = "\n".join(f"--- page {i+1} ---\n" + (pg.extract_text() or "") for i, pg in enumerate(pdf.pages))
open(f"data/interim/text/{os.path.splitext(os.path.basename(p))[0]}.txt", "w").write(t)
print(t[:mx])
