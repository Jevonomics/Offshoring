import numpy as np
"""Extract HCLTech metrics from investor releases (FY16-FY27). Tables carry explicit date headers ('30-Sep-25'),
so values map directly to calendar quarter ends. Later releases win for the same quarter/variable.
Writes data/interim/vendor_long_hcltech.csv (fiscal_label = Indian Apr-Mar FY derived from calendar date)."""
import glob, os, re, sys, datetime as dt, pdfplumber, pandas as pd
sys.path.insert(0, "src"); from vendor_common import write_long
DATE = r"\d{1,2}-[A-Z][a-z]{2}-\d{2,4}"
NUM = r"\(?-?[\d,]+(?:\.\d+)?%?\)?"
def cal(d):
    for f in ("%d-%b-%y", "%d-%b-%Y"):
        try: return dt.datetime.strptime(d, f).date()
        except ValueError: pass
def fiscal(d):  # Indian FY label from calendar quarter end
    fy = d.year + 1 if d.month >= 4 else d.year; q = {6: 1, 9: 2, 12: 3, 3: 4}[d.month]; return f"Q{q}FY{fy%100:02d}"
def num(t): neg = t.startswith("(") or t.startswith("-"); v = float(t.strip("()%-").replace(",", "")); return -v if neg else v
LAB = [(r"^revenue \(\$ ?mn\)$", "revenue_usd_m", "USD_m", "reported_table"),
       (r"^revenues$", "revenue_usd_m", "USD_m", None),
       (r"^total (employee|people) count$", "headcount_total", "persons", None),
       (r"^gross addition$", "gross_hires", "persons", None), (r"^freshers added$", "fresher_hires", "persons", None),
       (r"^net addition$", "net_addition", "persons", None),
       (r"^attrition.*(ltm)", "attrition_ltm", "pct", None)]
MIXLAB = {"americas", "usa", "europe", "row", "india", "application services", "infrastructure services", "business services",
          "engineering and r&d services", "it and business services", "products & platforms", "hclsoftware", "digital business"}
rows = []
for f in sorted(glob.glob("data/raw/hcltech/releases/*.pdf")):
    with pdfplumber.open(f) as pdf:
        for pi, pg in enumerate(pdf.pages):
            text = pg.extract_text() or ""
            usd_page = bool(re.search(r"\(IFRS\)|US GAAP|in \$|\$ ?Mn|US\$", text)) and not re.search(r"₹|Crore|crore|Ind AS", text)
            dates, mix, reported, prev, recent, tbl = [], False, False, "", [], 0
            for line in text.splitlines():
                ds = re.findall(DATE, line)
                if len(ds) >= 2:
                    raw = [cal(d) for d in ds]; dup = len(set(raw)) < len(raw)
                    dates = raw[:len(set(raw))] if dup else raw
                    # share tables: header says Mix (or a recent heading does), or a 'Details ... CC Growth' header; never growth tables with repeated dates
                    mix = (not (dup and len(set(raw)) < 3 and "Revenues" not in line)) and bool(
                        re.search(r"(?i)mix", line + " " + " ".join(recent[-3:])) or re.match(r"Details\s", line))
                    reported = "REPORTED" in line; tbl += 1; continue
                if not re.search(NUM + r"\s*$", line): recent.append(line)
                m = re.match(r"^(.*?[A-Za-z\)\*&])\s+(" + NUM + r"(?:\s+" + NUM + r")*)\s*$", line)
                if not m or not dates: continue
                label = re.sub(r"\s*\([A-D](\s*\+.*)?\)\s*$", "", m.group(1)).strip(); key = label.lower().rstrip("*").strip()
                vals = [num(t) for t in m.group(2).split()]
                hit = None
                for pat, var, unit, cond in LAB:
                    if re.search(pat, key) and (cond is None or (cond == "reported_table" and reported) or (cond == "usd_page" and usd_page)):
                        hit = (var, unit); break
                if not hit and mix and key in MIXLAB and "%" in m.group(2):
                    hit = (f"rev_share_mix:{label}", "pct")
                if not hit or len(vals) < len(dates): continue
                if hit[0] == "revenue_usd_m" and not all(1000 < v < 6000 for v in vals[:len(dates)]): continue  # USD quarterly; INR crore > 8,000
                for d, v in zip(dates, vals):
                    rows.append(dict(cal=d, variable=hit[0], unit=hit[1], value=v, src=f, loc=f"p{pi+1}: {line[:80]}", tbl=f"{pi}-{tbl}"))
df = pd.DataFrame(rows)
# share sets must sum to 100±1 within one table (screens out segment margin tables that share the labels)
REG = {"americas", "usa", "europe", "row", "india"}
sh = df.variable.str.startswith("rev_share_mix")
df["kind"] = np.where(df.variable.str.split(":").str[1].str.lower().isin(REG), "reg", "seg")
tot = df[sh].groupby(["src", "tbl", "cal", "kind"]).value.transform("sum")
df = df[~sh | tot.reindex(df.index).between(99, 101)]
# new geography scheme (USA/Europe/ROW/India, services basis, from Mar 2024) reuses 'Europe'/'ROW': tag them so schemes never mix
lab = df.variable.str.split(":").str[1]
newtab = df[lab.isin(["USA", "India"])].set_index(["src", "tbl", "cal"]).index
isnew = df.set_index(["src", "tbl", "cal"]).index.isin(newtab) & lab.isin(["Europe", "ROW"]).values
df.loc[isnew, "variable"] = df.loc[isnew, "variable"] + " [svc]"
df = df.drop(columns=["tbl", "kind"])
df = df.sort_values("src").drop_duplicates(subset=["cal", "variable"], keep="last")
out = [["HCLTech", fiscal(r.cal), r.cal.isoformat(), "", r.variable, r.value, r.unit, "reported", r.src, r.loc] for r in df.itertuples()]
d = write_long(out, "hcltech")
print(d.groupby("variable").agg(first=("cal_quarter_end","min"), last=("cal_quarter_end","max"), n=("value","size")).to_string())
