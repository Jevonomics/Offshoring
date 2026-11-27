"""Reconcile Test 1 (US imports from India above trend) with the six vendors' slow growth.
Compares, by calendar year, BEA US imports from India (computer & business services) with the six firms'
North America revenue. Not a pre-registered test; context for H1.
- North America revenue = quarterly US$ revenue x NA (or Americas) share, summed over the calendar year.
- HCLTech switched from "Americas" to "USA" in 2025 Q2; USA shares are scaled up by the Americas/USA ratio over the
  five overlap quarters (2024 Q1-2025 Q1) so the series stays on an Americas basis.
- LTIMindtree only from 2022 (combined history); window is 2022-2025 so all six firms are covered.
Caveat: vendor revenue includes onsite work done in the US (not an import) and Canada/Latin America for the
"Americas" firms, so levels are not comparable; only changes are compared."""
import pandas as pd
B = pd.read_csv("data/processed/bea_imports.csv")
b = B[(B.affiliation == "AllAffiliations") & (B.country == "India") & B.service_type.isin(["TelecomCompAndInfo", "OtherBusiness"])]
imp = b.pivot_table(index="year", columns="service_type", values="value_usd_m").sum(axis=1).rename("bea_india_cbs_usd_m")
V = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"])
S = pd.read_csv("data/processed/vendor_segments.csv", parse_dates=["cal_quarter_end"])
h = S[(S.firm == "HCLTech") & (S.segment_type == "region") & S.segment_label.isin(["Americas", "USA"])] \
    .pivot_table(index="cal_quarter_end", columns="segment_label", values="share_pct").dropna()
ratio = (h.Americas / h.USA).mean()
usa = (V.firm == "HCLTech") & (V.na_definition == "USA")
V.loc[usa, "na_share_pct"] *= ratio
V["yr"] = V.cal_quarter_end.dt.year
V["na_usd_m"] = V.revenue_usd_m * V.na_share_pct / 100
six = ["TCS", "Infosys", "Wipro", "HCLTech", "TechM", "LTIMindtree"]
g = V[V.firm.isin(six) & V.yr.between(2022, 2025)].groupby(["yr", "firm"]).agg(na=("na_usd_m", "sum"), n=("na_usd_m", "count"))
assert (g.n == 4).all(), g[g.n != 4]
na = g.na.unstack()
T = pd.concat([imp.loc[2022:2025], na.sum(axis=1).rename("six_firms_na_usd_m"), na], axis=1)
T.round(0).to_csv("outputs/reconcile_imports_vs_vendors.csv")
d = T.loc[2025] - T.loc[2022]; pct = 100 * (T.loc[2025] / T.loc[2022] - 1)
print(f"HCLTech Americas/USA ratio: {ratio:.3f}")
print((T / 1000).round(2).to_string())
print(pd.DataFrame({"change_2022_25_usd_bn": (d / 1000).round(2), "change_pct": pct.round(1)}).to_string())

# GCC proxy: majority-owned foreign affiliates (MOFAs) of US multinationals in India, BEA AMNE (outward), 2009-2024.
# Includes GCCs and US-owned vendors (e.g., Cognizant); serves all markets, not only the US. Raw: data/raw/bea_mne/.
import json
def mne(f, country="India"):
    d = json.load(open(f))["BEAAPI"]["Results"]["Data"]; df = pd.DataFrame(d)
    df = df[(df.Row == country) & df.Column.isin(["All Industries Total", "Information", "Professional, scientific, and technical services"])]
    return df.assign(v=pd.to_numeric(df.DataValueUnformatted, errors="coerce")).pivot_table(index="Year", columns="Column", values="v")
emp = mne("data/raw/bea_mne/outward_mofa_series8_india.json").add_prefix("employment_k: ")
comp = mne("data/raw/bea_mne/outward_mofa_series7.json").add_prefix("compensation_usd_m: ")
M = pd.concat([emp, comp], axis=1); M.index = M.index.astype(int); M.to_csv("outputs/us_affiliates_india.csv")
print(M.loc[2015:].to_string())
import numpy as np
for c in M.columns:
    y = np.log(M.loc[2015:2022, c]); b = np.polyfit(y.index, y.values, 1)
    print(f"{c}: 2024 vs 2015-22 trend {100 * (M.loc[2024, c] / np.exp(np.polyval(b, 2024)) - 1):+.1f}%; growth 2022-24 {100 * (M.loc[2024, c] / M.loc[2022, c] - 1):+.1f}%")
