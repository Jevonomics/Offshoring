"""Accenture quarterly revenue by type of work from the 'TYPE OF WORK' table (US$ thousands) in each earnings release:
current quarter, year-ago (restated, same definitions), and YoY growth in USD and local currency (LC).
Consulting = unexposed; Outsourcing (to FY22) / Managed Services (FY23+, incl. technology managed services + Operations/BPO) = exposed."""
import glob, html, os, re, pandas as pd
P = r"\(?(—|-?[\d,]+)\)?\s*%?"
rows = []
for f in sorted(glob.glob("data/raw/sec/accenture/*.htm")):
    t = html.unescape(re.sub(r"<[^>]+>", " ", open(f, encoding="utf-8", errors="ignore").read())); t = re.sub(r"\s+", " ", t)
    m = re.search(r"TYPE OF WORK Consulting \$ ([\d,]+) \$ ([\d,]+) (\(?[\d—-]+\)?) ?% (\(?[\d—-]+\)?) ?% (Outsourcing|Managed [Ss]ervices)(?: \(\d\))? ([\d,]+) ([\d,]+) (\(?[\d—-]+\)?) (\(?[\d—-]+\)?)", t)
    if not m: print("NO TABLE", os.path.basename(f)); continue
    g = lambda s: 0.0 if s in ("—", "-") else float(s.strip("()").replace(",", "")) * (-1 if s.startswith("(") else 1)
    # quarter end: release date ~3-4 weeks after Nov 30 / Feb 28 / May 31 / Aug 31
    fd = pd.Timestamp(os.path.basename(f)[:10]); qe = (fd - pd.offsets.MonthEnd(1)) if fd.day > 14 else (fd - pd.offsets.MonthEnd(2))
    qe = [d for d in pd.date_range(fd - pd.Timedelta(days=75), fd, freq="ME") if d.month in (2, 5, 8, 11)][-1]
    rows.append(dict(quarter_end=qe.date(), file_date=fd.date(), consulting_k=g(m.group(1)), consulting_yago_k=g(m.group(2)),
        consulting_yoy_usd=g(m.group(3)), consulting_yoy_lc=g(m.group(4)), second_label=m.group(5), managed_k=g(m.group(6)), managed_yago_k=g(m.group(7)),
        managed_yoy_usd=g(m.group(8)), managed_yoy_lc=g(m.group(9)), source=f))
d = pd.DataFrame(rows).sort_values("quarter_end"); d.to_csv("data/processed/accenture_type_of_work.csv", index=False)
print(d.drop(columns=["source", "file_date"]).to_string(index=False))
