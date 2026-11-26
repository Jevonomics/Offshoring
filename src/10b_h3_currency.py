"""H3 currency check: remove the euro's moves from Europe revenue and rerun the H3 regression and event study.
Europe revenue is converted at constant EUR/USD: EU_cc = EU_usd / fx_q, so log(NA/EU_cc) = y + s*log(fx_q)
(the base rate drops out with the firm-definition fixed effects). s = share of Europe revenue assumed billed in euros.
Main: s = 1 (all Europe revenue in euros). Caveat: firms don't report the euro/pound/other split; the pound moved
less than the euro in 2025, so s = 1 may over-correct. s = 0.5 shown as a sensitivity check.
FX: ECB reference rate, US$ per euro, monthly average (data/raw/fx/ecb_eurusd_monthly.csv), averaged to quarters."""
import sys, numpy as np, pandas as pd, statsmodels.formula.api as smf; sys.path.insert(0, "src"); from analysis_common import *
fx = pd.read_csv("data/raw/fx/ecb_eurusd_monthly.csv", usecols=["TIME_PERIOD", "OBS_VALUE"])
fx["m"] = pd.PeriodIndex(fx.TIME_PERIOD, freq="M"); fxq = fx.groupby(fx.m.dt.asfreq("Q")).OBS_VALUE.mean()
fxq.rename("usd_per_eur").to_frame().assign(q=lambda d: d.index.astype(str)).to_csv("outputs/h3_eurusd_quarterly.csv", index=False)
P = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"])
P = P[P.cal_quarter_end >= "2015-06-30"].dropna(subset=["na_share_pct", "europe_share_pct"]).copy()
P["firm_def"] = P.firm + " | " + P.na_definition
P["y0"] = np.log(P.na_share_pct / P.europe_share_pct)
P["lfx"] = np.log(P.cal_quarter_end.dt.to_period("Q").map(fxq))
assert P.lfx.notna().all(), P[P.lfx.isna()].cal_quarter_end.unique()
P["post"] = (P.cal_quarter_end >= POST).astype(int); P["post23"] = (P.cal_quarter_end >= POST_ROBUST).astype(int)
P["t"] = P.cal_quarter_end.dt.year + (P.cal_quarter_end.dt.quarter - 1) / 4
P["yr"] = P.cal_quarter_end.dt.year
P["firm_c"] = P.firm.replace({"LTI (standalone)": "LTIM", "LTIMindtree": "LTIM"})
def fit(f, d): return smf.ols(f, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.firm_c)[0]})
specs = [("main (post=2024Q1+)", "y ~ post + C(firm_def)", lambda d: d),
         ("robust: post=2023Q1+", "y ~ post23 + C(firm_def)", lambda d: d),
         ("robust: firm-specific linear trends", "y ~ post + C(firm_def) + C(firm_def):t", lambda d: d),
         ("robust: clean North America only (TCS, Infosys, LTI/LTIM)", "y ~ post + C(firm_def)", lambda d: d[d.na_definition == "North America"])]
out, ev = [], []
for s, label in [(0, "reported US$"), (0.5, "half of Europe in euros"), (1, "all Europe in euros (main)")]:
    P["y"] = P.y0 + s * P.lfx
    for name, f, sub in specs:
        d = sub(P); m = fit(f, d); k = "post23" if "post23" in f else "post"
        out.append(dict(adjustment=label, spec=name, coef_log_pts=100 * m.params[k], se=100 * m.bse[k], p=m.pvalues[k], n=int(m.nobs)))
    es = fit("y ~ C(yr, Treatment(2023)) + C(firm_def)", P)
    for y in range(2015, 2027):
        key = f"C(yr, Treatment(2023))[T.{y}]"
        ev.append(dict(adjustment=label, year=y, coef=0 if y == 2023 else 100 * es.params[key], se=0 if y == 2023 else 100 * es.bse[key]))
R = pd.DataFrame(out).round(3); R.to_csv("outputs/h3_currency_regression.csv", index=False); print(R.to_string(index=False))
E = pd.DataFrame(ev).round(2); E.to_csv("outputs/h3_currency_event_study.csv", index=False)
print(E.pivot(index="year", columns="adjustment", values="coef").to_string())
print(fxq["2022Q1":].round(3).to_string())
