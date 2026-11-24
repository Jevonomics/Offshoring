"""Extract Infosys quarterly metrics from user-supplied fact sheets (untrusted PDFs, text only via pdfplumber).
Column conventions (verified on FY16, FY21, FY27 layouts):
  metric tables: [current Q, previous Q, year-ago Q, (LTM/YTD...)]
  IFRS income statement 'Revenues' (US$ mn): [current Q, year-ago Q, growth, previous Q, growth]
Writes data/interim/vendor_long_infosys.csv. Each value is tagged with its column role; panel build prefers 'current'."""
import glob, os, re, sys
sys.path.insert(0, "src"); from vendor_common import fy_q_to_cal, write_long; from pdf_lines import pdf_lines
FILES = {"infosys_2015.pdf": (2015, 1), "infosys_2019.pdf": (2019, 2), "infosys_2024.pdf": (2024, 2), "infosys_2027.pdf": (2027, 2)}
for f in glob.glob("data/raw/manual/infosys/infosys_q*fy*.pdf"):
    m = re.search(r"q(\d)fy(\d\d)", f); FILES[os.path.basename(f)] = (2000 + int(m.group(2)), int(m.group(1)))
def shift(fy, q, k):  # k quarters back
    n = fy * 4 + (q - 1) - k; return n // 4, n % 4 + 1
NUM = r"\(?-?\d[\d,]*(?:\.\d+)?%?\)?"
def heal(s):
    """Rejoin digits split by stray spaces in some PDFs: '5 9.6'->'59.6', '1 00.0'->'100.0', '9 .6'->'9.6', '4 ,718'->'4,718', '( 2.1)'->'(2.1)'."""
    s = re.sub(r"\(\s+", "(", s)
    toks, out = s.split(), []
    for t in toks:
        if out and re.fullmatch(r"\(?\d", out[-1]) and re.match(r"[\d.,]", t): out[-1] += t
        else: out.append(t)
    return " ".join(out)
def nums(s):
    out = []
    for t in re.findall(NUM, heal(s)):
        neg = t.startswith("("); v = float(t.strip("()%").replace(",", "")); out.append(-v if neg else v)
    return out
def split_label(line):
    m = re.search(r"\s" + NUM + r"(\s|$)", " " + line)
    i = m.start() if m else len(line) + 1
    return line[:max(i - 1, 0)], line[max(i - 1, 0):]
GEO = {"northamerica": "North America", "europe": "Europe", "restoftheworld": "Rest of world", "india": "India"}
EMP = {"totalemployees": ("headcount_total", "persons"), "grossaddition": ("gross_hires", "persons")}
rows = []
for fn, (fy, q) in sorted(FILES.items()):
    path = f"data/raw/manual/infosys/{fn}"; section = ""
    for page, line in pdf_lines(path):
        label, rest = split_label(line); key = re.sub(r"[^a-z]", "", label.lower()); vals = nums(rest)
        if key.startswith("revenuesby") or key.startswith("revenueby"): section = key; continue
        recs = []
        if "geograph" in section and key in GEO and len(vals) >= 3: recs = [(f"rev_share_region:{GEO[key]}", "pct", vals[:3])]
        elif key in EMP and len(vals) >= 3: recs = [(*EMP[key], vals[:3])]
        elif "attrition" in key and "%" in rest and len(vals) >= 3: recs = [(f"attrition[{label.strip()}]", "pct", vals[:3])]
        elif key.endswith("includingtrainees") and len(vals) >= 3: recs = [("utilization_incl_trainees", "pct", vals[:3])]
        elif key.endswith("excludingtrainees") and len(vals) >= 3: recs = [("utilization_excl_trainees", "pct", vals[:3])]
        elif key == "revenues" and len(vals) >= 4 and 1000 <= vals[0] <= 9000 and 1000 <= vals[3] <= 9000 and abs(vals[2]) < 60:
            recs = [("revenue_usd_m", "USD_m", [vals[0], vals[3], vals[1]])]  # reorder to current, previous, year-ago
        for var, unit, v3 in recs:
            for k, (role, v) in enumerate(zip(["current", "previous", "year_ago"], v3)):
                f2, q2 = shift(fy, q, [0, 1, 4][k])
                rows.append(["Infosys", f"Q{q2}FY{f2%100:02d}", fy_q_to_cal(f2, q2), role, var, v, unit, "reported", path, f"p{page}: {line[:90]}"])
df = write_long(rows, "infosys")
df = df.drop_duplicates(subset=["fiscal_label", "variable", "section", "source_file"])
cur = df[df.section == "current"]
print(cur.groupby("variable").agg(first=("cal_quarter_end","min"), last=("cal_quarter_end","max"), n_files=("value","size")).to_string())
print("files:", len(FILES))
