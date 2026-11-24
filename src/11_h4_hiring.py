"""H4: Are post-2024 headcount declines driven by lower hiring with steady attrition, or by layoffs?
Implied gross hires = net change + leavers, leavers ~= attrition rate (annual, %) x average headcount / 4.
Attrition definitions differ by firm and over time, so comparisons are within firm only."""
import sys, numpy as np, pandas as pd; sys.path.insert(0, "src"); from analysis_common import *
P = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"]).sort_values(["firm", "cal_quarter_end"])
P = P[P.firm.isin(["TCS", "Infosys", "Wipro", "HCLTech", "TechM", "LTIMindtree"])].copy()
P["net"] = P.groupby("firm").headcount_total.diff(); P["avg_hc"] = P.groupby("firm").headcount_total.transform(lambda s: (s + s.shift()) / 2)
P["leavers"] = P.attrition_pct / 100 * P.avg_hc / 4; P["hires_implied"] = P.net + P.leavers
P["hire_rate_ann"] = 400 * P.hires_implied / P.avg_hc; P["net_rate_ann"] = 400 * P.net / P.avg_hc
LAY = pd.read_csv("data/processed/layoff_events.csv", parse_dates=["period_affected_start", "period_affected_end"])
P["layoff_window"] = False
for e in LAY.itertuples(): P.loc[(P.firm == e.firm) & P.cal_quarter_end.between(e.period_affected_start, e.period_affected_end + pd.Timedelta(days=1)), "layoff_window"] = True
base = P[P.cal_quarter_end.between("2016-04-01", "2019-12-31")]  # pre-boom baseline
b = base.groupby("firm").agg(base_attr=("attrition_pct", "mean"), base_attr_sd=("attrition_pct", "std"), base_hire=("hire_rate_ann", "mean"), base_net=("net_rate_ann", "mean"))
post = P[P.cal_quarter_end >= POST].merge(b, on="firm")
def classify(r):
    if r.net >= 0 or pd.isna(r.net): return "no decline"
    if r.layoff_window: return "decline during announced layoff"
    if pd.isna(r.attrition_pct): return "decline, attrition unknown"
    if r.attrition_pct > r.base_attr + 2 * r.base_attr_sd: return "decline with unusually high attrition"
    return "decline from low hiring (attrition normal or low)" if r.hire_rate_ann < r.base_hire else "decline, hiring not below baseline"
post["class"] = post.apply(classify, axis=1)
post[["firm", "fiscal_label", "cal_quarter_end", "headcount_total", "net", "attrition_pct", "attrition_definition", "hire_rate_ann", "base_hire", "base_attr", "layoff_window", "class"]].round(2).to_csv("outputs/h4_quarter_classification.csv", index=False)
C = post.groupby(["firm", "class"]).size().unstack(fill_value=0); print(C.to_string()); print("\nTotal:", post["class"].value_counts().to_dict())
S = P.assign(period=np.select([P.cal_quarter_end.between("2016-04-01", "2019-12-31"), P.cal_quarter_end.between("2021-01-01", "2022-12-31"), P.cal_quarter_end >= POST], ["2016-19 baseline", "2021-22 boom", "2024+ post"], "other"))
S = S[S.period != "other"].groupby(["firm", "period"]).agg(attrition=("attrition_pct", "mean"), hire_rate=("hire_rate_ann", "mean"), net_rate=("net_rate_ann", "mean")).round(1).unstack()
S.to_csv("outputs/h4_period_summary.csv"); print(S.to_string())
# Fresher hires where disclosed (HCLTech FY22+), annual totals
fr = P[P.fresher_hires.notna()].assign(fy=lambda d: np.where(d.cal_quarter_end.dt.month >= 4, d.cal_quarter_end.dt.year + 1, d.cal_quarter_end.dt.year))
print("\nHCLTech freshers by FY:", fr[fr.firm == "HCLTech"].groupby("fy").fresher_hires.agg(["sum", "count"]).to_dict("index"))
# Chart 5: six firms combined (excluding TCS layoff quarters shown separately): hires vs leavers vs net, annualized % of headcount
A = P[P.cal_quarter_end >= "2016-06-30"].dropna(subset=["hires_implied", "leavers"]).groupby("cal_quarter_end").agg(hires=("hires_implied", "sum"), leavers=("leavers", "sum"), net=("net", "sum"), hc=("avg_hc", "sum"), n=("firm", "nunique"))
A = A[A.n >= 5]
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(A.index, 400 * A.hires / A.hc, color="#3d6a99", lw=2, label="Hires (implied)"); ax.plot(A.index, 400 * A.leavers / A.hc, color="#e8a33d", lw=2, label="Leavers (attrition)")
ax.bar(A.index, 400 * A.net / A.hc, width=60, color=np.where(A.net < 0, "#c0392b", "#7fb77e"), label="Net change")
ax.axhline(0, color="#333", lw=.6); mark_periods(ax); style(ax); ax.set_ylabel("% of headcount, annualized"); ax.legend(frameon=False, fontsize=8)
ax.set_title("Since 2024, hiring and quitting both fell; hiring fell to about the quit rate, so headcount is flat", loc="left", fontsize=11, weight="bold")
fig.text(0, -.04, "Five-to-six largest Indian IT firms combined (quarters with ≥5 firms reporting). Hires = net change + attrition × avg headcount ÷ 4; firm attrition definitions differ. "
         "TCS layoffs (~12,261, Jul 2025–Mar 2026) fall inside the post-period. Source: company fact sheets.", fontsize=7.3, color="#555")
save(fig, "05_hiring_pipeline")
