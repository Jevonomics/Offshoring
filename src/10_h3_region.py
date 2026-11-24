"""H3: North America vs Europe. With two segments per firm-quarter, the pre-registered spec
log(seg_rev) ~ NA x post + firm x segment FE + firm x quarter FE  is equivalent to
y = log(NA_rev / EU_rev) = log(NA_share / EU_share) ~ post + firm-definition FE.  SEs clustered by firm.
Also: event study by calendar year (ref 2023), per-firm before/after growth gaps, robustness (2023 post; firm trends; TCS constant currency)."""
import sys, numpy as np, pandas as pd, statsmodels.formula.api as smf; sys.path.insert(0, "src"); from analysis_common import *
P = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"])
P = P[P.cal_quarter_end >= "2015-06-30"].dropna(subset=["na_share_pct", "europe_share_pct"]).copy()
P["firm_def"] = P.firm + " | " + P.na_definition
P["y"] = np.log(P.na_share_pct / P.europe_share_pct)
P["post"] = (P.cal_quarter_end >= POST).astype(int); P["post23"] = (P.cal_quarter_end >= POST_ROBUST).astype(int)
P["t"] = P.cal_quarter_end.dt.year + (P.cal_quarter_end.dt.quarter - 1) / 4
P["firm_c"] = P.firm.replace({"LTI (standalone)": "LTIM", "LTIMindtree": "LTIM"})  # cluster at company level
def fit(formula, d): return smf.ols(formula, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.firm_c)[0]})
out = []
for name, f, d in [("main (post=2024Q1+)", "y ~ post + C(firm_def)", P),
                   ("robust: post=2023Q1+", "y ~ post23 + C(firm_def)", P),
                   ("robust: firm-specific linear trends", "y ~ post + C(firm_def) + C(firm_def):t", P),
                   ("robust: clean North America only (TCS, Infosys, LTI/LTIM)", "y ~ post + C(firm_def)", P[P.na_definition == "North America"])]:
    m = fit(f, d); k = "post23" if "post23" in f else "post"
    out.append(dict(spec=name, coef_log_pts=100 * m.params[k], se=100 * m.bse[k], p=m.pvalues[k], n=int(m.nobs), clusters=d.firm_c.nunique()))
R = pd.DataFrame(out).round(3); R.to_csv("outputs/h3_regression.csv", index=False); print(R.to_string(index=False))
# Event study by calendar year, reference 2023
P["yr"] = P.cal_quarter_end.dt.year
es = fit("y ~ C(yr, Treatment(2023)) + C(firm_def)", P)
E = pd.DataFrame({"year": range(2015, 2027)}); E["coef"] = [0 if y == 2023 else 100 * es.params.get(f"C(yr, Treatment(2023))[T.{y}]", np.nan) for y in E.year]
E["se"] = [0 if y == 2023 else 100 * es.bse.get(f"C(yr, Treatment(2023))[T.{y}]", np.nan) for y in E.year]
E.round(2).to_csv("outputs/h3_event_study.csv", index=False); print(E.round(2).to_string(index=False))
# Per-firm simple comparison: avg YoY growth of implied NA revenue minus Europe revenue, pre (2016-2023) vs post (2024+)
P = P.sort_values(["firm_def", "cal_quarter_end"])
P["na_rev"] = P.na_share_pct / 100 * P.revenue_usd_m; P["eu_rev"] = P.europe_share_pct / 100 * P.revenue_usd_m
for c in ("na_rev", "eu_rev"): P[c + "_yoy"] = 100 * P.groupby("firm_def")[c].pct_change(4, fill_method=None)
P["gap"] = P.na_rev_yoy - P.eu_rev_yoy
F = P.dropna(subset=["gap"]).groupby(["firm", "na_definition"]).apply(lambda g: pd.Series({
    "pre_gap_pp": g[(g.cal_quarter_end < POST) & (g.yr >= 2016)].gap.mean(), "post_gap_pp": g[g.cal_quarter_end >= POST].gap.mean()}), include_groups=False).reset_index()
F["change_pp"] = F.post_gap_pp - F.pre_gap_pp; F.round(2).to_csv("outputs/h3_per_firm.csv", index=False); print(F.round(2).to_string(index=False))
# TCS constant-currency check (reported CC YoY growth by region)
L = pd.read_csv("data/interim/vendor_long_tcs.csv", parse_dates=["cal_quarter_end"])
cc = L[L.variable.str.startswith("rev_cc_growth_yoy_region")].pivot_table(index="cal_quarter_end", columns="variable", values="value") * 100
cc["na_minus_europe_cc"] = cc["rev_cc_growth_yoy_region:North America"] - (cc["rev_cc_growth_yoy_region:UK"] + cc["rev_cc_growth_yoy_region:Continental Europe"]) / 2
tcs = pd.Series({"pre (2016-2023) avg NA-minus-Europe CC growth gap, pp": cc[(cc.index < POST) & (cc.index >= "2016-01-01")].na_minus_europe_cc.mean(),
                 "post (2024+) avg gap, pp": cc[cc.index >= POST].na_minus_europe_cc.mean()}).round(2)
tcs.to_csv("outputs/h3_tcs_constant_currency.csv"); print(tcs.to_string())
# Chart 4: NA minus Europe YoY growth gap (all firms, 4-quarter avg) + event study panel
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.4), gridspec_kw={"width_ratios": [1.5, 1]})
for fd, g in P.dropna(subset=["gap"]).groupby("firm_def"):
    a1.plot(g.cal_quarter_end, g.gap.rolling(4, min_periods=2).mean(), lw=1.4, label=fd.replace(" | ", ": "))
a1.axhline(0, color="#333", lw=.7); mark_periods(a1); style(a1); a1.set_ylabel("NA growth − Europe growth, pp (4-qtr avg)")
a1.legend(frameon=False, fontsize=6.5, ncol=2, loc="lower left"); a1.set_title("Growth gap by firm (US$, reported)", loc="left", fontsize=10)
a2.errorbar(E.year, E.coef, yerr=1.96 * E.se, fmt="o", color="#c0392b", capsize=3); a2.axhline(0, color="#333", lw=.7); a2.axvline(2023.5, color="#888", ls=":")
style(a2); a2.set_title("Event study: NA/Europe ratio vs 2023 (log pts, 95% CI)", loc="left", fontsize=10)
c = R.iloc[0]; fig.suptitle(f"North America vs Europe: a small drift toward Europe after 2024 ({c.coef_log_pts:+.0f} log pts), not statistically distinguishable from zero (p={c.p:.2f})" if c.coef_log_pts < 0 else
    f"North America vs Europe: no relative decline for North America after 2024 ({c.coef_log_pts:+.0f} log pts, p={c.p:.2f})", x=.01, ha="left", weight="bold", fontsize=11.5)
fig.text(.01, -.03, "Implied regional revenue = share × US$ revenue. 'Americas' for TechM/HCLTech/Wipro (incl. Canada & LatAm). US$ figures include currency effects: a weaker dollar raises Europe's US$ revenue. Source: company fact sheets.", fontsize=7.3, color="#555")
fig.tight_layout(rect=(0, .02, 1, .93)); save(fig, "04_na_vs_europe"); save_es = E
