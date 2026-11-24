"""H1: log-linear trend on 2015-2022, projected 2023+ with 95% prediction intervals.
Outputs: outputs/h1_trend_gaps.csv, outputs/charts/01_bea_imports_trend.{png,svg}"""
import numpy as np, pandas as pd, statsmodels.api as sm, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
TREND = (2015, 2022); MIN_PTS = 6
df = pd.read_csv("data/processed/bea_imports.csv")
df = df[df.affiliation == "AllAffiliations"]
# Headline series: "computer and business services" = Telecom/computer/info + Other business services (both must be published)
w = df.pivot_table(index=["country", "year"], columns="service_type", values="value_usd_m")
comb = (w["TelecomCompAndInfo"] + w["OtherBusiness"]).dropna().rename("value_usd_m").reset_index()
comb["service_type"] = "CompAndBusiness"
TYPES = ["AllTypesOfService", "CompAndBusiness", "TelecomCompAndInfo", "Comp", "OtherBusiness",
         "ProfMgmtConsult", "TechTradeRelatedOth", "ResearchAndDev", "PotIctEnServ"]
d = pd.concat([df[["country", "year", "service_type", "value_usd_m"]], comb])
d = d[d.service_type.isin(TYPES) & d.value_usd_m.gt(0)]

def fit(s):
    tr = s[(s.year >= TREND[0]) & (s.year <= TREND[1])]
    if len(tr) < MIN_PTS: return None
    m = sm.OLS(np.log(tr.value_usd_m), sm.add_constant(tr.year.astype(float))).fit()
    yrs = np.arange(TREND[0], s.year.max() + 1)
    pr = m.get_prediction(sm.add_constant(yrs.astype(float))).summary_frame(alpha=0.05)
    pr["year"] = yrs
    return m, pr

res, paths = [], {}
for (c, t), s in d.groupby(["country", "service_type"]):
    s = s.sort_values("year"); f = fit(s)
    if f is None:
        res.append(dict(country=c, service_type=t, note=f"<{MIN_PTS} published years in trend window; not fitted")); continue
    m, pr = f; paths[(c, t)] = (s, pr)
    for _, p in pr[pr.year > TREND[1]].iterrows():
        a = s.loc[s.year == p.year, "value_usd_m"]
        act = a.iloc[0] if len(a) else np.nan
        res.append(dict(country=c, service_type=t, year=int(p.year), actual=act, trend=np.exp(p["mean"]),
            gap_pct=100 * (act / np.exp(p["mean"]) - 1),
            pi_lo_gap_pct=100 * (act / np.exp(p.obs_ci_upper) - 1), pi_hi_gap_pct=100 * (act / np.exp(p.obs_ci_lower) - 1),
            outside_95pi_below=act < np.exp(p.obs_ci_lower), outside_95pi_above=act > np.exp(p.obs_ci_upper),
            trend_growth_pct=100 * (np.exp(m.params.iloc[1]) - 1), n_trend_pts=int(m.nobs)))
r = pd.DataFrame(res)
# Benchmark: country gap minus All-countries gap, in log points
g = r.dropna(subset=["year"]).copy(); g["log_gap"] = np.log1p(g.gap_pct / 100)
b = g[g.country == "AllCountries"][["service_type", "year", "log_gap"]].rename(columns={"log_gap": "bench_log_gap"})
r = r.merge(b, on=["service_type", "year"], how="left")
r["rel_to_allcountries_pts"] = 100 * (np.log1p(r.gap_pct / 100) - r.bench_log_gap)
r.drop(columns="bench_log_gap").round(2).to_csv("outputs/h1_trend_gaps.csv", index=False)

# Chart 1
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
for ax, c, name in zip(axes, ["India", "Philippines"], ["India", "Philippines"]):
    s, pr = paths[(c, "CompAndBusiness")]
    s = s[s.year >= 2010]
    ax.fill_between(pr.year, np.exp(pr.obs_ci_lower) / 1e3, np.exp(pr.obs_ci_upper) / 1e3, color="#9bb7d4", alpha=.35, lw=0, label="2015–22 trend, 95% band")
    ax.plot(pr.year, np.exp(pr["mean"]) / 1e3, color="#3d6a99", ls="--", lw=1.5, label="Trend")
    ax.plot(s.year, s.value_usd_m / 1e3, color="#c0392b", marker="o", ms=3.5, lw=2, label="Actual")
    ax.axvspan(2023.5, s.year.max() + .5, color="#eee", zorder=0); ax.axvline(2022.9, color="#888", lw=.8, ls=":")
    ax.text(2022.85, ax.get_ylim()[1] * .97, "ChatGPT\n(Nov 2022)", ha="right", va="top", fontsize=8, color="#555")
    ax.text(2024.0, ax.get_ylim()[1] * .90, "post-\nperiod", ha="center", va="top", fontsize=8, color="#555")
    ax.set_title(f"{name}", loc="left", fontsize=11); ax.set_ylabel("US$ bn, nominal"); ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(2009.5, s.year.max() + .5)
axes[0].legend(frameon=False, fontsize=8, loc="upper left")
fig.suptitle("US imports of computer & business services: India ran above its 2015–22 trend after 2023; the Philippines fell below", x=.01, ha="left", fontsize=13, weight="bold")
fig.text(.01, .005, "Computer & business services = 'telecom, computer & information services' + 'other business services'. "
         "Source: BEA International Services (IntlServTrade), all affiliations, nominal.", fontsize=7.5, color="#555")
fig.tight_layout(rect=(0, .03, 1, .95))
for ext in ("png", "svg"): fig.savefig(f"outputs/charts/01_bea_imports_trend.{ext}", dpi=160)
print(r.drop(columns="bench_log_gap").round(1).to_string(index=False))
