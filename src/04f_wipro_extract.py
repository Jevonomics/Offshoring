"""Build Wipro long file from (a) EDGAR HTML datasheets (data/interim/wipro_raw.csv; FY16Q4-FY21Q2) and
(b) wipro.com datasheet PDFs (FY22Q1-FY27Q2). Later documents win for the same quarter/variable.
Writes data/interim/vendor_long_wipro.csv."""
import glob, os, re, sys, pandas as pd
sys.path.insert(0, "src"); from vendor_common import fy_q_to_cal, write_long
import pdfplumber
def text_lines(path):
    with pdfplumber.open(path) as pdf:
        return [(i + 1, ln) for i, pg in enumerate(pdf.pages) for ln in (pg.extract_text() or '').splitlines()]
def var_for(section, label):
    label = re.sub(r"\s*Note\s*[\d&]+$", "", label.replace("\xa0", " ")).strip()
    s, l = section.lower(), re.sub(r"\s*note\s*[\d&]+", "", label.lower()).strip()
    if "earlier segment" in l: return None
    if l.startswith("it services revenues") or l.startswith("it services revenues ($mn) revised"): return ("revenue_it_usd_m", "USD_m")
    if l == "closing employee count": return ("headcount_total", "persons")
    if l.startswith("net utilization (excluding trainees)"): return ("utilization_excl_trainees", "pct")
    if l.startswith("gross utilization"): return ("utilization_gross", "pct")
    if l.startswith("voluntary ttm"): return ("attrition_ltm_it_voluntary", "pct")
    if re.match(r"(bps|do&?p) ?%.*post training quarterly", l): return ("attrition_bps_post_training_qtr", "pct")
    l = l.replace("americas_one", "americas 1").replace("americas_two", "americas 2")
    if l in ("americas", "europe", "americas 1", "americas 2", "apmea", "india & middle east business", "apac and other emerging markets", "rest of the world"):
        return (f"rev_share_region:{label.strip().replace('_One', ' 1').replace('_Two', ' 2')}", "pct")
    if l in ("digital operations and platforms", "cloud and infrastructure services", "modern application services",
             "data, analytics and ai", "industrial & engineering services", "business application services",
             "global infrastructure services", "business process services", "product engineering services", "product engineering",
             "analytics", "consulting", "application services"):
        return (f"rev_share_service_line:{label}", "pct")
    return None
rows = []
# (a) HTML era
raw = pd.read_csv("data/interim/wipro_raw.csv")
for r in raw.itertuples():
    v = var_for(str(r.section) if isinstance(r.section, str) else "", r.label)
    if v: rows.append(dict(fy=r.fy, q=r.q, variable=v[0], unit=v[1], value=r.value, file_date=r.file_date, source_file=r.file, locator=f"table {r.table}: {r.label}"))
# (b) website PDFs
NUM = r"-?[\d,]+(?:\.\d+)?%?"
for f in sorted(glob.glob("data/raw/wipro/datasheet-q*fy*.pdf")):
    m = re.search(r"q(\d)fy(\d\d)", f); q, fy = int(m.group(1)), 2000 + int(m.group(2))
    hdr = (["FY", "Q4", "Q3", "Q2", "Q1", "FY", "Q4"] if q == 4 else [f"Q{k}" for k in range(q, 0, -1)] + ["FY", "Q4", "Q3", "Q2", "Q1"])
    cols, y = [], fy
    for i, t in enumerate(hdr):
        if t == "FY" and i > 0: y -= 1
        cols.append(None if t == "FY" else (y, int(t[1])))
    seen = set()
    for page, line in text_lines(f):
        line = re.sub(r"(?i)\bamericas 1\b", "Americas_One", re.sub(r"(?i)\bamericas 2\b", "Americas_Two", line))
        mm = re.match(r"^(.*?[A-Za-z\)])\s+(" + NUM + r"(?:\s+" + NUM + r")+)\s*$", line)
        if not mm: continue
        v = var_for("", mm.group(1))
        if not v or v[0] in seen: continue
        seen.add(v[0])
        vals = [float(x.strip("%").replace(",", "")) for x in mm.group(2).split()]
        for c, val in zip(cols, vals):
            if c: rows.append(dict(fy=c[0], q=c[1], variable=v[0], unit=v[1], value=val, file_date=f"{fy}Q{q}", source_file=f, locator=f"p{page}: {line[:80]}"))
df = pd.DataFrame(rows)
df["fd_key"] = df.file_date.astype(str)
df = df.sort_values("fd_key").drop_duplicates(subset=["fy", "q", "variable"], keep="last")  # latest document wins
out = [["Wipro", f"Q{r.q}FY{r.fy%100:02d}", fy_q_to_cal(int(r.fy), int(r.q)), "", r.variable, r.value, r.unit, "reported", r.source_file, r.locator] for r in df.itertuples()]
d = write_long(out, "wipro")
print(d.groupby("variable").agg(first=("cal_quarter_end","min"), last=("cal_quarter_end","max"), n=("value","size")).to_string())
