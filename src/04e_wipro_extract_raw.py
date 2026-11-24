"""Parse every Wipro EDGAR datasheet exhibit into long raw rows (section, label, FY, Q, value).
Header rows give fiscal year ('FY 16-17') and quarter ('Q4'/'FY') per column. Writes data/interim/wipro_raw.csv."""
import glob, io, os, re, pandas as pd
rows = []
for f in sorted(glob.glob("data/raw/sec/wipro_datasheets/*.htm")):
    fd = os.path.basename(f)[:10]
    try: tables = pd.read_html(io.StringIO(open(f, encoding="utf-8", errors="ignore").read()))
    except ValueError: print("NO TABLES:", os.path.basename(f)); continue
    for ti, t in enumerate(tables):
        if t.shape[1] < 6: continue
        t = t.astype(object).where(t.notna(), None).values.tolist()
        fyrow = qrow = None
        for i, r in enumerate(t):
            cells = [str(c) for c in r if c is not None]
            if any(re.search(r"FY\s?\d{2}\s?[-–]\s?\d{2}", c) for c in cells): fyrow, qrow = r, t[i + 1] if i + 1 < len(t) else None; continue
            if fyrow is None or qrow is None or r is qrow: continue
            texts = [c for c in r[:4] if isinstance(c, str) and not re.fullmatch(r"[\d.,%()\-–\s]*", c)]
            if not texts: continue
            section, label = (texts[0], texts[-1]) if len(texts) > 1 else ("", texts[0])
            for j, c in enumerate(r):
                if j < 2 or c is None: continue
                s = str(c).replace(",", "").strip()
                if not re.fullmatch(r"\(?-?\d+(\.\d+)?\)?", s): continue
                fy = re.search(r"FY\s?(\d{2})\s?[-–]\s?(\d{2})", str(fyrow[j]) if j < len(fyrow) else "")
                qq = str(qrow[j]).strip() if j < len(qrow) and qrow[j] is not None else ""
                if not fy or not re.fullmatch(r"Q[1-4]", qq): continue
                v = float(s.strip("()")) * (-1 if s.startswith("(") else 1)
                rows.append(dict(file_date=fd, file=f, table=ti, section=section.strip(), label=label.strip(),
                                 fy=2000 + int(fy.group(2)), q=int(qq[1]), value=v))
df = pd.DataFrame(rows).drop_duplicates()
df.to_csv("data/interim/wipro_raw.csv", index=False)
print(len(df), "values from", df.file.nunique(), "files")
lab = df.groupby(["section", "label"]).agg(n_files=("file", "nunique"), first=("fy", "min"), last=("fy", "max")).reset_index()
pd.set_option("display.width", 250); print(lab.sort_values(["section", "first"]).to_string(index=False, max_colwidth=60))
