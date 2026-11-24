"""H5: US computer systems design employment vs its 2015-2022 trend (monthly, SA)."""
import sys, numpy as np, pandas as pd; sys.path.insert(0, "src"); from analysis_common import *
b = pd.read_csv("data/processed/bls.csv", parse_dates=["date"])
res = []
for sid, g in b.groupby("series_id"):
    g = g.sort_values("date").reset_index(drop=True); t = g.date.dt.year + (g.date.dt.month - 1) / 12
    fit = (g.date >= "2015-01-01") & (g.date <= "2022-12-01")
    m, tr = loglin_trend(t, g.value, fit.values); g = pd.concat([g, tr], axis=1)
    for yr in (2023, 2024, 2025, 2026):
        h = g[g.date.dt.year == yr]
        res.append(dict(series=g.series.iloc[0], year=yr, months=len(h), actual_avg=h.value.mean(), trend_avg=h.trend.mean(),
                        gap_pct=100 * (h.value.mean() / h.trend.mean() - 1), below_95pi_months=int((h.value < h.pi_lo).sum()),
                        above_95pi_months=int((h.value > h.pi_hi).sum()), trend_growth_pct_yr=100 * (np.exp(np.asarray(m.params)[1]) - 1)))
    if sid == "CES6054150001": main = g
r = pd.DataFrame(res).round(2); r.to_csv("outputs/h5_bls_gaps.csv", index=False); print(r.to_string(index=False))
fig, ax = plt.subplots(figsize=(8.5, 4.2)); g = main[main.date >= "2014-01-01"]
ax.fill_between(g.date, g.pi_lo, g.pi_hi, color="#9bb7d4", alpha=.35, lw=0, label="2015–22 trend, 95% band")
ax.plot(g.date, g.trend, ls="--", color="#3d6a99", lw=1.3, label="Trend"); ax.plot(g.date, g.value, color="#c0392b", lw=2, label="Actual")
mark_periods(ax); style(ax); ax.set_ylabel("Employees, thousands (SA)"); ax.legend(frameon=False, fontsize=8, loc="upper left")
last = r[(r.series.str.contains("5415")) & (r.year == 2026)].iloc[0]
ax.set_title(f"US computer systems design jobs are {abs(last.gap_pct):.0f}% {'below' if last.gap_pct < 0 else 'above'} their 2015–22 trend in 2026", loc="left", fontsize=11, weight="bold")
fig.text(0, -.02, "NAICS 5415, all employees, seasonally adjusted. Source: BLS Current Employment Statistics (CES6054150001). Dotted line: ChatGPT release; shaded: post-period (2024+).", fontsize=7.5, color="#555")
save(fig, "08_h5_us_it_jobs")
