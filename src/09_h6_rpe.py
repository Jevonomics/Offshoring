"""H6 (Channel B): revenue per employee vs FY16-FY22 trend, plus robustness and headcount decomposition."""
import sys, numpy as np, pandas as pd; sys.path.insert(0, "src"); from analysis_common import *
P = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"]).sort_values(["firm", "cal_quarter_end"])
P["avg_hc"] = P.groupby("firm").headcount_total.transform(lambda s: (s + s.shift()) / 2)
P["rpe_k"] = P.revenue_usd_m * 4 / P.avg_hc * 1000  # annualized US$ thousand per employee
P["t"] = P.cal_quarter_end.dt.year + (P.cal_quarter_end.dt.quarter - 1) / 4
SPECS = {"main FY16-FY22": ("2015-06-30", "2022-03-31"), "excl. 2021-22 hiring boom": ("2015-06-30", "2020-12-31"), "from 2019": ("2019-03-31", "2022-03-31")}
FIRMS = ["TCS", "Infosys", "Wipro", "HCLTech", "TechM", "LTI (standalone)", "LTIMindtree"]
rows, paths = [], {}
for f in FIRMS:
    g = P[(P.firm == f) & P.rpe_k.notna()].reset_index(drop=True)
    for spec, (a, b) in SPECS.items():
        fit = ((g.cal_quarter_end >= a) & (g.cal_quarter_end <= b)).values
        if fit.sum() < 8: continue
        m, tr = loglin_trend(g.t, g.rpe_k, fit); h = pd.concat([g, tr], axis=1)
        if spec.startswith("main"): paths[f] = h
        post = h[h.cal_quarter_end >= POST]
        rows.append(dict(firm=f, spec=spec, n_fit=int(fit.sum()), trend_growth_pct_yr=100 * (np.exp(4 * 0 + np.asarray(m.params)[1]) - 1),
            post_quarters=len(post), mean_gap_pct=100 * (post.rpe_k / post.trend - 1).mean() if len(post) else np.nan,
            latest_gap_pct=100 * (post.rpe_k.iloc[-1] / post.trend.iloc[-1] - 1) if len(post) else np.nan,
            share_post_above_95pi=(post.rpe_k > post.pi_hi).mean() if len(post) else np.nan,
            share_post_below_95pi=(post.rpe_k < post.pi_lo).mean() if len(post) else np.nan,
            fy21_covid_gap_pct=100 * (h[h.cal_quarter_end.between("2020-06-30", "2021-03-31")].rpe_k / h[h.cal_quarter_end.between("2020-06-30", "2021-03-31")].trend - 1).mean(),
            fy17_gap_pct=100 * (h[h.cal_quarter_end.between("2016-06-30", "2017-03-31")].rpe_k / h[h.cal_quarter_end.between("2016-06-30", "2017-03-31")].trend - 1).mean()))
R = pd.DataFrame(rows).round(2); R.to_csv("outputs/h6_rpe_gaps.csv", index=False); print(R.to_string(index=False))
pd.concat([h.assign(firm=f)[["firm", "cal_quarter_end", "rpe_k", "trend", "pi_lo", "pi_hi"]] for f, h in paths.items()]).round(3) \
    .to_csv("outputs/h6_rpe_paths.csv", index=False)   # main-spec paths, for the Ramp chart
# Chart 6: small multiples, main spec (LTIMindtree too short to fit -> LTI shown)
show = [f for f in FIRMS if f in paths]
fig, axes = plt.subplots(2, 3, figsize=(12, 6.4), sharex=True); axes = axes.ravel()
for ax, f in zip(axes, show[:6]):
    h = paths[f]; ax.fill_between(h.cal_quarter_end, h.pi_lo, h.pi_hi, color="#9bb7d4", alpha=.35, lw=0)
    ax.plot(h.cal_quarter_end, h.trend, ls="--", color="#3d6a99", lw=1.2); ax.plot(h.cal_quarter_end, h.rpe_k, color="#c0392b", lw=1.8)
    mark_periods(ax); style(ax); ax.set_title(f, loc="left", fontsize=10); ax.set_xlim(pd.Timestamp("2015-01-01"), pd.Timestamp("2026-12-31"))
for ax in axes[::3]: ax.set_ylabel("US$ '000 per employee")
main = R[R.spec.str.startswith("main")]
above = (main.mean_gap_pct > 0).sum()
fig.suptitle(f"Channel B · Revenue per employee vs 2016–22 trend: {above} of {len(main)} firms above trend after 2024", x=.01, ha="left", weight="bold", fontsize=12)
fig.text(.01, -.01, "Annualized quarterly USD revenue ÷ average headcount. Dashed: FY16–FY22 log-linear trend with 95% band. Shaded: post-period (2024+). "
         "LTI = standalone pre-merger (ends Sep 2022). Source: company fact sheets.", fontsize=7.5, color="#555")
fig.tight_layout(rect=(0, .02, 1, .95)); save(fig, "06_rev_per_employee")
# Decomposition (FY, firms with 4 complete quarters): dlog headcount = dlog revenue - dlog RPE
P["fy"] = np.where(P.cal_quarter_end.dt.month >= 4, P.cal_quarter_end.dt.year + 1, P.cal_quarter_end.dt.year)
D4 = ["TCS", "Infosys", "HCLTech", "TechM"]
A = P[P.firm.isin(D4)].groupby(["fy", "firm"]).agg(rev=("revenue_usd_m", "sum"), nq=("revenue_usd_m", "count"), hc_end=("headcount_total", "last")).reset_index()
A = A[A.nq == 4].groupby("fy").filter(lambda g: len(g) == len(D4)).groupby("fy")[["rev", "hc_end"]].sum()
A["dlog_rev"] = 100 * np.log(A.rev).diff(); A["dlog_hc"] = 100 * np.log(A.hc_end).diff(); A["dlog_rpe"] = A.dlog_rev - A.dlog_hc
A = A.dropna().round(2); A.to_csv("outputs/h6_decomposition.csv"); print(A.to_string())
fig, ax = plt.subplots(figsize=(9, 4.4)); x = A.index.astype(str)
ax.bar(x, A.dlog_rev, color="#3d6a99", label="Revenue growth (log pts)"); ax.bar(x, -A.dlog_rpe, bottom=0, color="#e8a33d", alpha=.85, label="minus revenue-per-employee growth")
ax.plot(x, A.dlog_hc, "ko-", ms=4, lw=1.2, label="= Headcount growth"); ax.axhline(0, color="#333", lw=.6); style(ax); ax.legend(frameon=False, fontsize=8)
ax.set_title("Headcount growth = revenue growth − productivity growth (TCS, Infosys, HCLTech, TechM combined)", loc="left", fontsize=10.5, weight="bold")
ax.set_xlabel("Indian fiscal year (Apr–Mar); FY26 = Apr 2025–Mar 2026"); fig.text(0, -.04, "US$ revenue summed over four quarters; year-end headcount. Source: company fact sheets.", fontsize=7.5, color="#555")
save(fig, "07_decomposition")
