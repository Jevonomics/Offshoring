"""H2 (LIMITED, fallbacks approved by user): exposed vs unexposed work.
 (a) Accenture: Managed services/Outsourcing (exposed) vs Consulting (unexposed), YoY local-currency growth (restated year-ago basis).
 (b) TechM: BPS headcount (exposed) vs software headcount (mixed), YoY growth.
 (c) HCLTech: IT & Business Services (mostly exposed, ambiguous) vs Engineering & R&D (unexposed), implied US$ revenue YoY growth.
 (d) BEA India/Philippines imports by type: exposed vs unexposed buckets vs 2015-22 trend.
Outcome per series: gap = exposed growth - unexposed growth (pp); compare post (2024Q1+) to pre (2016-2023), with past downturns shown.
Pooled: gap ~ post + firm FE, Newey-West (4 lags) SEs since only 3 series (clustering infeasible)."""
import sys, numpy as np, pandas as pd, statsmodels.formula.api as smf; sys.path.insert(0, "src"); from analysis_common import *
G = []
A = pd.read_csv("data/processed/accenture_type_of_work.csv", parse_dates=["quarter_end"])
G.append(pd.DataFrame({"series": "Accenture: Managed svcs − Consulting (LC growth)", "q": A.quarter_end, "gap": A.managed_yoy_lc - A.consulting_yoy_lc}))
P = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"]); T = P[P.firm == "TechM"].set_index("cal_quarter_end").sort_index()
g = 100 * (T.headcount_bps.pct_change(4, fill_method=None) - T.headcount_software.pct_change(4, fill_method=None))
G.append(pd.DataFrame({"series": "TechM: BPS − software headcount growth", "q": g.index, "gap": g.values}))
S = pd.read_csv("data/processed/vendor_segments.csv", parse_dates=["cal_quarter_end"])
H = S[(S.firm == "HCLTech") & S.segment_label.isin(["IT and Business Services", "Engineering and R&D Services"])].pivot_table(index="cal_quarter_end", columns="segment_label", values="implied_revenue_usd_m")
g = 100 * (H["IT and Business Services"].pct_change(4, fill_method=None) - H["Engineering and R&D Services"].pct_change(4, fill_method=None))
G.append(pd.DataFrame({"series": "HCLTech: ITBS − Engineering & R&D revenue growth (US$)", "q": g.index, "gap": g.values}))
G = pd.concat(G).dropna(); G = G[G.q >= "2016-01-01"]; G["post"] = (G.q >= POST).astype(int)
def per(d):
    m = smf.ols("gap ~ post", d).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    win = lambda a, b: d[d.q.between(a, b)].gap.mean()
    return pd.Series({"n": len(d), "pre_mean_pp": d[d.post == 0].gap.mean(), "post_mean_pp": d[d.post == 1].gap.mean(), "change_pp": m.params["post"],
        "se": m.bse["post"], "p": m.pvalues["post"], "fy17_slowdown_pp": win("2016-06-01", "2017-06-30"), "covid_2020_pp": win("2020-04-01", "2021-03-31"),
        "post_2023_robust_pp": d[d.q >= POST_ROBUST].gap.mean()})
R = G.groupby("series").apply(per, include_groups=False).round(2); print(R.to_string())
pool = smf.ols("gap ~ post + C(series)", G).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
R.loc["POOLED (series FE, HAC)", ["n", "change_pp", "se", "p"]] = [len(G), round(pool.params["post"], 2), round(pool.bse["post"], 2), round(pool.pvalues["post"], 3)]
# Robustness (DECISIONS 2026-11-26): TechM's software staff are arguably exposed too, so pool without it.
G2 = G[~G.series.str.startswith("TechM")]
pool2 = smf.ols("gap ~ post + C(series)", G2).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
R.loc["POOLED without TechM (robustness)", ["n", "change_pp", "se", "p"]] = [len(G2), round(pool2.params["post"], 2), round(pool2.bse["post"], 2), round(pool2.pvalues["post"], 3)]
R.to_csv("outputs/h2_vendor_proxies.csv"); print(R.tail(1).to_string())
# (d) BEA by type
B = pd.read_csv("data/processed/bea_imports.csv"); B = B[(B.affiliation == "AllAffiliations") & B.year.between(2015, 2025)]
BUCKETS = {"India": {"exposed": ["Comp", "AccountAuditBookkeep", "Legal"], "unexposed": ["ResearchAndDev", "ArchEngSciAndOthTech", "BusMgmtConsPubRel"]},
           "Philippines": {"exposed": ["TelecomCompAndInfo", "AccountAuditBookkeep", "Legal"], "unexposed": ["ResearchAndDev", "ArchEngSciAndOthTech", "BusMgmtConsPubRel"]}}
rows = []
for c, bk in BUCKETS.items():
    for lab, types in bk.items():
        v = B[(B.country == c) & B.service_type.isin(types)].pivot_table(index="year", columns="service_type", values="value_usd_m")
        complete = v.notna().all(axis=1); s = v.sum(axis=1).where(complete)
        d = s.dropna(); fit = (d.index <= 2022)
        if fit.sum() < 6: rows.append(dict(country=c, bucket=lab, note=f"too few complete pre years ({fit.sum()})")); continue
        m, tr = loglin_trend(d.index.values, d.values, fit)
        for yr in (2023, 2024, 2025):
            if yr in d.index: i = list(d.index).index(yr); rows.append(dict(country=c, bucket=lab, types="+".join(types), year=yr, actual=d.loc[yr], trend=tr.trend.iloc[i],
                gap_pct=100 * (d.loc[yr] / tr.trend.iloc[i] - 1), outside_95=("below" if d.loc[yr] < tr.pi_lo.iloc[i] else "above" if d.loc[yr] > tr.pi_hi.iloc[i] else "inside"), pre_years=int(fit.sum())))
BE = pd.DataFrame(rows).round(1); BE.to_csv("outputs/h2_bea_by_type.csv", index=False); print(BE.to_string(index=False))
# Chart 3
fig, ax = plt.subplots(figsize=(10, 4.6)); cols = ["#3d6a99", "#e8a33d", "#7fb77e"]
for (s, d), c in zip(G.groupby("series"), cols): ax.plot(d.q, d.gap.rolling(2, min_periods=1).mean(), color=c, lw=1.8, label=s)
ax.axhline(0, color="#333", lw=.7); mark_periods(ax); style(ax); ax.set_ylabel("Exposed minus unexposed YoY growth, pp"); ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.set_title("H2 (limited): exposed work did not fall behind unexposed work after 2024 in any proxy", loc="left", fontsize=11, weight="bold")
fig.text(0, -.04, "Above zero = exposed work growing faster. Accenture: local currency, restated year-ago. TechM: headcount. HCLTech: implied US$ revenue; ITBS mixes exposed and unexposed work. "
         "Shaded: 2024+. Sources: Accenture 8-K earnings releases; company fact sheets.", fontsize=7.3, color="#555")
save(fig, "03_exposed_vs_unexposed")
