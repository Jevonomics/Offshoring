"""H1 robustness: trend window 2015-2021 (drops the 2022 Philippines jump) and 2015-2019 (pre-COVID), vs main 2015-2022."""
import sys, numpy as np, pandas as pd; sys.path.insert(0, "src"); from analysis_common import loglin_trend
B = pd.read_csv("data/processed/bea_imports.csv"); B = B[(B.affiliation == "AllAffiliations") & B.year.between(2015, 2025)]
SER = {"CompAndBusiness": ["TelecomCompAndInfo", "OtherBusiness"], "TelecomCompAndInfo": ["TelecomCompAndInfo"], "OtherBusiness": ["OtherBusiness"], "AllTypesOfService": ["AllTypesOfService"]}
rows = []
for c in ["India", "Philippines", "AllCountries"]:
    for name, types in SER.items():
        v = B[(B.country == c) & B.service_type.isin(types)].pivot_table(index="year", columns="service_type", values="value_usd_m")
        s = v.sum(axis=1).where(v.notna().all(axis=1) & (v.shape[1] == len(types))).dropna()
        for win, end in [("2015-22 (main)", 2022), ("2015-21", 2021), ("2015-19", 2019)]:
            fit = (s.index <= end)
            if fit.sum() < 5: continue
            m, tr = loglin_trend(s.index.values, s.values, fit); tr.index = s.index
            for yr in (2024, 2025):
                if yr in s.index: rows.append(dict(country=c, series=name, window=win, year=yr, gap_pct=100 * (s[yr] / tr.trend[yr] - 1),
                    band=("below" if s[yr] < tr.pi_lo[yr] else "above" if s[yr] > tr.pi_hi[yr] else "inside")))
R = pd.DataFrame(rows).round(1)
bench = R[R.country == "AllCountries"].set_index(["series", "window", "year"]).gap_pct
R["vs_allcountries_pp"] = (R.gap_pct - R.set_index(["series", "window", "year"]).index.map(bench).values).round(1)
R.to_csv("outputs/h1_robustness.csv", index=False)
print(R[R.year == 2025].pivot_table(index=["country", "series"], columns="window", values=["gap_pct"], aggfunc="first").to_string())
print(R[(R.year == 2025)].pivot_table(index=["country", "series"], columns="window", values="band", aggfunc="first").to_string())
