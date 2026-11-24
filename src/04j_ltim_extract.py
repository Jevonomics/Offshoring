"""Extract LTI (standalone, pre-merger docs FY17Q1-FY23Q2) and LTIMindtree (combined, docs FY23Q3+, which restate
history to Q1 FY22) from ltm.com fact sheets. Headers are quarter labels ('Q2FY16', 'Q2 FY26', 'Q2 FY 2 3').
Writes data/interim/vendor_long_lti.csv and vendor_long_ltimindtree.csv."""
import glob, os, re, sys, pdfplumber, pandas as pd
sys.path.insert(0, "src"); from vendor_common import fy_q_to_cal, write_long
QT = r"Q([1-4])\s*FY\s*(\d)\s*(\d)"
NUM = r"\(?-?[\d,]+(?:\.\d+)?%?\)?"
def num(t): neg = t.startswith("("); v = float(t.strip("()%").replace(",", "")); return -v if neg else v
LAB = [(r"^revenue\s*(\(usd (million|mn)\)|usd \$? ?mn)$", "revenue_usd_m", "USD_m"),
       (r"^north america$", "rev_share_region:North America", "pct"), (r"^europe$", "rev_share_region:Europe", "pct"),
       (r"^(rest of (the )?world|row)$", "rev_share_region:Rest of world", "pct"), (r"^india$", "rev_share_region:India", "pct"),
       (r"^total (headcount|employees)$", "headcount_total", "persons"),
       (r"^(attrition % \(ltm\)|ttm attrition %)$", "attrition_ltm", "pct"),
       (r"^utili[sz]ation \(excl ?\. trainees\)( %)?$", "utilization_excl_trainees", "pct")]
rows = []
for f in sorted(glob.glob("data/raw/ltim/factsheets/FY*_Q*.pdf")):
    fy, q = map(int, re.search(r"FY(\d{4})_Q(\d)", f).groups())
    entity = "LTIMindtree" if (fy, q) >= (2023, 3) else "LTI"
    with pdfplumber.open(f) as pdf:
        for pi, pg in enumerate(pdf.pages):
            cols, hdr = [], ""
            for line in (pg.extract_text() or "").splitlines():
                qs = re.findall(QT, line)
                if len(qs) >= 2:
                    seen, cols = set(), []
                    for a, b, c in qs:  # keep first run of distinct quarters (some headers repeat the run twice)
                        k = (2000 + int(b + c), int(a))
                        if k in seen: break
                        seen.add(k); cols.append(k)
                    hdr = line; continue
                m = re.match(r"^(.*?[A-Za-z\)%])\s+(" + NUM + r"(?:\s+" + NUM + r")*)(?:\s+\D.*)?$", line)
                if not m or not cols: continue
                key = re.sub(r"\s+", " ", m.group(1).lower()).strip()
                hit = next(((v, u) for pat, v, u in LAB if re.search(pat, key)), None)
                if not hit and key == "revenue" and re.search(r"In USD Mn", hdr): hit = ("revenue_usd_m", "USD_m")
                vals = [num(t) for t in m.group(2).split()]
                if not hit or len(vals) < len(cols): continue
                if hit[0].startswith("rev_share") and "%" not in m.group(2): continue
                for (fy2, q2), v in zip(cols, vals):
                    rows.append(dict(entity=entity, fy=fy2, q=q2, variable=hit[0], unit=hit[1], value=v, doc=(fy, q), src=f, loc=f"p{pi+1}: {line[:80]}"))
df = pd.DataFrame(rows).sort_values("doc").drop_duplicates(subset=["entity", "fy", "q", "variable"], keep="last")
for ent, fn in [("LTI", "lti"), ("LTIMindtree", "ltimindtree")]:
    d = df[df.entity == ent]
    out = [[ent, f"Q{r.q}FY{r.fy%100:02d}", fy_q_to_cal(r.fy, r.q), "", r.variable, r.value, r.unit, "reported", r.src, r.loc] for r in d.itertuples()]
    x = write_long(out, fn); print(f"=== {ent}"); print(x.groupby("variable").agg(first=("cal_quarter_end","min"), last=("cal_quarter_end","max"), n=("value","size")).to_string())
