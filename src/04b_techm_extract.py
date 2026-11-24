"""Extract Tech Mahindra quarterly metrics from its cumulative datasheet (FY16 Q1 - FY27 Q2).
Writes data/interim/vendor_long_techm.csv."""
import re, sys, openpyxl
sys.path.insert(0, "src"); from vendor_common import fy_q_to_cal, write_long
SRC = "data/raw/techm/tml-q2-fy-27-datasheet.xlsx"
wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
rows = []
def periods(data):
    fyrow, qrow = data[0], data[1]; out = {}; fy = None
    for j, (a, b) in enumerate(zip(fyrow, qrow)):
        if isinstance(a, str) and (m := re.search(r"FY ?(\d{4})-(\d{2})", a)): fy = 2000 + int(m.group(2))
        if fy and isinstance(b, str) and re.fullmatch(r"Q[1-4]", b.strip()): out[j] = (fy, int(b.strip()[1]))
    return out
MAP = {"Revenue From Operations": ("revenue_usd_m", "USD_m"),
       "Software professionals": ("headcount_software", "persons"), "BPS professionals": ("headcount_bps", "persons"),
       "Sales & support": ("headcount_sales_support", "persons"), "Total Headcount": ("headcount_total", "persons"),
       "IT Attrition % (LTM) #": ("attrition_ltm_it", "share"), "IT Utilization % #": ("utilization_incl_trainees", "share"),
       "IT Utilization % (Excluding Trainees) #": ("utilization_excl_trainees", "share")}
for name in ["P&L US$ mn", "Operating Metrics "]:
    data = list(wb[name].iter_rows(values_only=True)); per = periods(data); section = ""
    for i, r in enumerate(data[2:], start=3):
        lab = r[0].strip() if isinstance(r[0], str) else None
        if not lab: continue
        # Known source error: on "Operating Metrics", FY2015-16 columns sit one row ABOVE their label (verified against
        # the Q1 FY17 PDF fact sheet). Take FY16 values from the row above. See DECISIONS.md.
        src_row = lambda j: data[i - 2] if (name == "Operating Metrics " and per[j][0] == 2016) else r
        nums = {j: src_row(j)[j] for j in per if isinstance(src_row(j)[j], (int, float))}
        if not any(isinstance(v, (int, float)) for j, v in enumerate(r) if j in per and per[j][0] != 2016) and not (name == "P&L US$ mn" and nums):
            section = lab; continue
        if "Geography" in section and lab in ("Americas", "Europe", "Rest of world"): var, unit = f"rev_share_region:{lab}", "share"
        elif "Industry" in section: var, unit = f"rev_share_industry[{section[:60]}]:{lab}", "share"
        elif lab in MAP and not (name == "P&L US$ mn" and lab != "Revenue From Operations"): var, unit = MAP[lab]
        else: continue
        if name == "Operating Metrics " and lab == "Revenue From Operations": continue
        for j, v in nums.items():
            fy, q = per[j]
            rows.append(["TechM", f"Q{q}FY{fy%100:02d}", fy_q_to_cal(fy, q), section, var, v, unit, "reported", SRC, f"{name.strip()}!R{i}C{j+1}"])
df = write_long(rows, "techm")
print(df[~df.variable.str.startswith("rev_share_industry")].groupby("variable").agg(first=("cal_quarter_end","min"), last=("cal_quarter_end","max"), n=("value","size"), last_val=("value","last")).to_string())
