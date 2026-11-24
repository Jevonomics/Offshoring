"""Strip HTML to text and grep for audit keywords. Usage: python -I src/01f_grep_docs.py <dir> [<dir>...]"""
import glob, html, re, sys
KW = r"(North America|Europe|Financial Services|segment|fresher|graduate|gross addition|utiliz|subcontract|attrition|headcount|total employees|business process|BPM|BPO|application development|consulting|infrastructure|service line|service offering)"
for d in sys.argv[1:]:
    for f in sorted(glob.glob(f"{d}/*.htm*")):
        if f.endswith("index.htm"): continue
        t = open(f, encoding="utf-8", errors="ignore").read()
        t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"\s+", " ", t)
        hits = {}
        for m in re.finditer(KW, t, re.I):
            k = m.group(1).lower(); hits.setdefault(k, t[max(0,m.start()-80):m.end()+120])
        print(f"\n### {f} ({len(t)} chars)")
        for k, v in hits.items(): print(f"  [{k}] …{v}…")
