"""Extract TCS quarterly metrics from the user-supplied Data Sheet (untrusted data, read-only via openpyxl).
Writes data/interim/vendor_long_tcs.csv."""
import re, sys, openpyxl
sys.path.insert(0, "src"); from vendor_common import fy_q_to_cal, write_long
SRC = "data/raw/manual/TCS-Data-Sheet-Q2FY27.xlsx"
wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
rows = []
def parse_period(p):
    m = re.fullmatch(r"([1-4])Q(\d{2})", str(p).strip())
    return (2000 + int(m.group(2)), int(m.group(1))) if m else None

def sheet_rows(name, keep_label):
    ws = wb[name]; data = list(ws.iter_rows(values_only=True)); hdr = data[0]; section = ""
    for i, r in enumerate(data[1:], start=2):
        lab = r[0].strip() if isinstance(r[0], str) else None
        if not lab: continue
        nums = [(j, v) for j, v in enumerate(r[1:], start=1) if isinstance(v, (int, float))]
        if not nums: section = lab; continue
        if not keep_label(section, lab): continue
        for j, v in nums:
            pq = parse_period(hdr[j]) if j < len(hdr) else None
            if pq: yield section, lab, pq, v, f"{name}!R{i}C{j+1}"

# Operating metrics: geography (new classification), YoY CC by geography, headcount, attrition, net addition, utilization
for section, lab, (fy, q), v, loc in sheet_rows("Operating Metrics", lambda s, l: True):
    s = section.lower()
    if "old classification" in s: continue
    if "geography - new" in s: var, unit = f"rev_share_region:{lab.rstrip(' *')}", "share"
    elif "yoy cc revenue growth by geography" in s: var, unit = f"rev_cc_growth_yoy_region:{lab}", "share"
    elif "service practice" in s and "growth" not in s: var, unit = f"rev_share_service_line:{lab}", "share"
    elif lab == "Total Headcount": var, unit = "headcount_total", "persons"
    elif lab == "Net Addition": var, unit = "net_addition", "persons"
    elif lab.startswith("Attrition : IT Services"): var, unit = "attrition_ltm_it", "share"
    elif lab.startswith("Attrition : Voluntary IT"): var, unit = "attrition_ltm_it_voluntary", "share"
    elif lab == "Excluding Trainees": var, unit = "utilization_excl_trainees", "share"
    elif lab == "Trainees" and "talent" in s: var, unit = "fresher_hires", "persons"
    elif lab == "Total Employees Recruited": var, unit = "gross_hires", "persons"
    else: continue
    rows.append(["TCS", f"Q{q}FY{fy%100:02d}", fy_q_to_cal(fy, q), section, var, v, unit, "reported", SRC, loc])

# USD P&L: historical (1Q11-FY26) then current (1Q26-2Q27); current sheet wins on overlap
pl = {}
for name in ["IFRS-PnL,BS-USD-Historical", "IFRS-PnL,BS-USD"]:
    for section, lab, (fy, q), v, loc in sheet_rows(name, lambda s, l: True):
        if "balance sheet" in section.lower(): continue
        if lab in ("Total Revenue", "Revenue"): var = "revenue_usd_m"
        elif lab.lower().startswith("fees to external consultants"): var = "subcontracting_cost_usd_m"
        else: continue
        key = (fy, q, var)
        if var == "subcontracting_cost_usd_m" and key in pl and pl[key][0] == name:
            pl[key] = (name, pl[key][1] + v, pl[key][2] + ";" + loc)  # historical sheet splits CoR and SG&A lines
        else: pl[key] = (name, v, loc)
for (fy, q, var), (name, v, loc) in pl.items():
    rows.append(["TCS", f"Q{q}FY{fy%100:02d}", fy_q_to_cal(fy, q), name, var, v, "USD_m", "reported", SRC, loc])
df = write_long(rows, "tcs")
print(df.groupby("variable").agg(first=("cal_quarter_end", "min"), last=("cal_quarter_end", "max"), n=("value", "size")).to_string())
