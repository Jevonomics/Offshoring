"""Re-draw every chart in the Ramp-AI-Index exhibit style -> outputs/charts/ramp/.
Reads the processed data and test outputs; recomputes only what the earlier scripts didn't save."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "src")
from exhibit import Exhibit, INK, SUB, GRID, ORANGE, NAVY, GRAY, BG, MARGIN
from analysis_common import loglin_trend, POST
import matplotlib.dates as mdates
from matplotlib.transforms import blended_transform_factory

OUT = "outputs/charts/ramp/"
CREDIT = "Analysis: Atharv Joshi"
LIGHT_O, LIGHT_N = "#f4c9ad", "#c3cde6"


def post_line(ax, x, label="AI coding tools\nspread (2024)", ymax=None):
    ax.axvline(x, color=SUB, ls=(0, (3, 3)), lw=1.1, zorder=1)
    if label:
        y = ax.get_ylim()[1] if ymax is None else ymax
        ax.annotate(label, (x, y), xytext=(-7, 0), textcoords="offset points", ha="right", va="top",
                    color=SUB, fontsize=12.5, linespacing=1.15)


def end_label(ax, x, y, text, color=INK, dx=6, dy=0):
    ax.annotate(text.replace("-", "−"), (x, y), xytext=(dx, dy), textcoords="offset points", va="center",
                fontsize=15, weight="bold", color=color)


def year_axis(ax):
    """A label for every year, two-digit style ('17) so they fit."""
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("'%y"))
    ax.tick_params(axis="x", labelsize=12.5)


def year_ticks(ax, years):
    ax.set_xticks(years); ax.set_xticklabels([f"'{y % 100:02d}" for y in years]); ax.tick_params(axis="x", labelsize=12.5)


def align_left(ex, ax, iters=4):
    """Shift the axes' left edge so its leftmost text (tick or row labels) lines up with the
    headline's left margin; the right edge stays put."""
    target = MARGIN / ex.w
    for _ in range(iters):
        ex.fig.canvas.draw()
        d = target - ax.get_tightbbox(ex._r).x0 / ex.fig.bbox.width
        if abs(d) < 2e-4: break
        pos = ax.get_position(); ax.set_position([pos.x0 + d, pos.y0, pos.width - d, pos.height])


def finish(ex, ax, name):
    align_left(ex, ax); ex.save(OUT + name)


# 01 · H1 BEA imports: one chart per country, levels vs 2015-22 trend ---------------------
B = pd.read_csv("data/processed/bea_imports.csv")
B = B[(B.affiliation == "AllAffiliations") & B.year.between(2015, 2025) & B.service_type.isin(["TelecomCompAndInfo", "OtherBusiness"])]
BEA_COUNTRY = {
    "India": dict(name="01a_bea_india", title=[[("US imports from ", INK), ("India", ORANGE), (" ran", INK)], [("24% above ", INK), ("trend", NAVY), (" in 2025", INK)]],
                  ylim=(0, 45), yt=[0, 10, 20, 30, 40],
                  note="Above the 95% band in 2025, and further above trend than imports from all countries (+14%). "
                       "With a pre-COVID trend (2015–19), India is on trend."),
    "Philippines": dict(name="01b_bea_philippines", title=[[("US imports from the ", INK), ("Philippines", ORANGE)], [("fell below ", INK), ("trend", NAVY), (", inside the band", INK)]],
                  ylim=(0, 12), yt=[0, 3, 6, 9, 12],
                  note="−30% vs trend in 2025, but inside the 95% band, and the sign flips with other trend windows. "
                       "A 2022 BEA category change (call-center work moving to management consulting) likely affects 2022–25."),
}
for c, cfg in BEA_COUNTRY.items():
    v = B[B.country == c].pivot_table(index="year", columns="service_type", values="value_usd_m")
    sr = v.sum(axis=1).where(v.notna().all(axis=1)).dropna() / 1000
    _, tr = loglin_trend(sr.index.values, sr.values, sr.index.values <= 2022); tr.index = sr.index
    ex = Exhibit(height=6.6)
    ex.title(cfg["title"])
    ex.subtitle("Computer & business services, US$ billions")
    ex.legend([("Actual", ORANGE), ("2015–22 trend", NAVY), ("95% band", LIGHT_N)])
    ex.source(cfg["note"] + " Nominal US$.",
              "Source: BEA International Services (telecom, computer & information + other business services).", credit=CREDIT)
    ax = ex.axes(left=0.1, right=0.86)
    ax.fill_between(sr.index, tr.pi_lo, tr.pi_hi, color=LIGHT_N, alpha=.6, lw=0, zorder=0)
    ax.plot(sr.index, tr.trend, color=NAVY, lw=2, ls=(0, (4, 3)), zorder=2)
    ax.plot(sr.index, sr.values, color=ORANGE, lw=2.8, zorder=3, marker="o", ms=5)
    hi = sr.values[-1] > tr.trend.values[-1]
    end_label(ax, 2025, sr.values[-1], f"{sr.values[-1]:.1f}", dy=6 if hi else -6)
    end_label(ax, 2025, tr.trend.values[-1], f"{tr.trend.values[-1]:.1f}", color=NAVY, dy=-6 if hi else 6)
    ax.set_ylim(*cfg["ylim"]); ax.set_yticks(cfg["yt"])
    ax.set_yticklabels([str(t) for t in cfg["yt"][:-1]] + [f"${cfg['yt'][-1]}bn"])
    ax.set_xlim(2014.5, 2025.5); year_ticks(ax, range(2015, 2026))
    post_line(ax, 2023.5, ymax=cfg["ylim"][1] * 0.99)
    finish(ex, ax, cfg["name"])

# 03 · H2 exposed vs unexposed: dumbbell before/after ------------------------------------
R = pd.read_csv("outputs/h2_vendor_proxies.csv").set_index("series")
rows = [("Accenture", "Managed services − consulting", "Accenture: Managed svcs − Consulting (LC growth)"),
        ("TechM", "BPO − software staff", "TechM: BPS − software headcount growth"),
        ("HCLTech", "IT & business − engineering", "HCLTech: ITBS − Engineering & R&D revenue growth (US$)")]
ex = Exhibit(height=6.6)
ex.title([[("Exposed work didn't fall", INK)], [("behind after 2024", INK)]])
ex.subtitle("Exposed minus unexposed growth, pp per year")
ex.legend([("2016–23 average", NAVY), ("2024+ average", ORANGE)])
ex.source("Above zero = AI-exposed work growing faster. Accenture in local currency; TechM headcount; HCLTech "
          "implied US$ revenue (its IT & business division mixes exposed and unexposed work). "
          "Pooled change −0.4 pp (p = 0.83). Stand-ins: no firm reports revenue by type of work after 2024.",
          "Source: Accenture 8-K earnings releases; Company fact sheets.", credit=CREDIT)
ax = ex.axes(left=0.40, right=0.70, bottom_pad=0.5)
COLS = blended_transform_factory(ex.fig.transFigure, ax.transData)   # columns pinned to the right margin
X_P = 1 - (MARGIN + 0.22) / ex.w; X_CH = X_P - 0.8 / ex.w
for i, (firm, lab, key) in enumerate(rows):
    r, y = R.loc[key], len(rows) - 1 - i
    ax.plot([r.pre_mean_pp, r.post_mean_pp], [y, y], color=GRID, lw=7, solid_capstyle="round", zorder=1)
    ax.scatter([r.pre_mean_pp], [y], s=150, color=NAVY, edgecolor="white", lw=1.8, zorder=3)
    ax.scatter([r.post_mean_pp], [y], s=150, color=ORANGE, edgecolor="white", lw=1.8, zorder=3)
    ax.text(-0.04, y + 0.16, firm, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=14, color=INK, weight="semibold")
    ax.text(-0.04, y - 0.19, lab, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=11, color=SUB)
    ax.text(X_CH, y, f"{r.change_pp:+.1f}".replace("-", "−"), transform=COLS, ha="center", va="center", fontsize=14, weight="bold")
    ax.text(X_P, y, f"{r.p:.2f}", transform=COLS, ha="center", va="center", fontsize=14, color=INK)
ax.text(X_CH, len(rows) - 0.35, "Change", transform=COLS, ha="center", va="bottom", fontsize=12.5, color=SUB, weight="semibold")
ax.text(X_P, len(rows) - 0.35, "p", transform=COLS, ha="center", va="bottom", fontsize=12.5, color=SUB, weight="semibold")
ax.set_ylim(-0.6, len(rows) - 0.4); ax.set_yticks([]); ax.set_xlim(-1.5, 11); ax.set_xticks([0, 2, 4, 6, 8, 10]); ax.tick_params(axis="x", labelsize=12.5)
ax.grid(axis="y", visible=False); ax.grid(axis="x", color=GRID, lw=1); ax.axvline(0, color=INK, lw=1.2)
ax.spines["bottom"].set_visible(False)
finish(ex, ax, "03_exposed_vs_unexposed")

# 04 · H3 event study --------------------------------------------------------------------
E = pd.read_csv("outputs/h3_event_study.csv")
ex = Exhibit(height=6.4)
ex.title([[("No clear shift from ", INK), ("North", ORANGE)], [("America", ORANGE), (" toward Europe", INK)]])
ex.subtitle("North America ÷ Europe revenue share, vs 2023, log points")
ex.legend([("Before 2024", NAVY), ("2024 onward", ORANGE), ("95% interval", GRAY)])
ex.source("Six firms (TCS, Infosys, Wipro, HCLTech, TechM, LTI/LTIMindtree), each compared with its own average. "
          "Pooled after-2024 shift −3.8 (p = 0.65). US$ basis: a weaker dollar in 2025 inflates Europe; "
          "TCS's constant-currency data move the other way.", "Source: Company fact sheets.", credit=CREDIT)
ax = ex.axes(left=0.13, right=0.95)
ax.vlines(E.year, E.coef - 1.96 * E.se, E.coef + 1.96 * E.se, color=GRAY, lw=3.5, zorder=1)
ax.scatter(E.year, E.coef, s=90, color=np.where(E.year >= 2024, ORANGE, NAVY), edgecolor="white", lw=1.5, zorder=3)
ax.axhline(0, color=INK, lw=1.2, zorder=2); ax.set_ylim(-25, 25); ax.set_yticks([-20, -10, 0, 10, 20])
ax.set_yticklabels(["−20", "−10", "0", "+10", "+20"]); year_ticks(ax, range(2015, 2027)); ax.set_xlim(2014.4, 2026.6)
ax.spines["bottom"].set_visible(False)
post_line(ax, 2023.5, ymax=24.5)
end_label(ax, 2026, E.coef.iloc[-1], f"{E.coef.iloc[-1]:+.0f}", dx=9)
finish(ex, ax, "04_na_vs_europe")

# 05 · H4 hiring vs leaving --------------------------------------------------------------
P = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"]).sort_values(["firm", "cal_quarter_end"])
P6 = P[P.firm.isin(["TCS", "Infosys", "Wipro", "HCLTech", "TechM", "LTIMindtree"])].copy()
P6["net"] = P6.groupby("firm").headcount_total.diff()
P6["avg_hc"] = P6.groupby("firm").headcount_total.transform(lambda s: (s + s.shift()) / 2)
P6["leavers"] = P6.attrition_pct / 100 * P6.avg_hc / 4; P6["hires"] = P6.net + P6.leavers
A = P6[P6.cal_quarter_end >= "2016-06-30"].dropna(subset=["hires", "leavers"]).groupby("cal_quarter_end").agg(
    hires=("hires", "sum"), leavers=("leavers", "sum"), hc=("avg_hc", "sum"), n=("firm", "nunique"))
A = A[A.n >= 5]; h, l = 400 * A.hires / A.hc, 400 * A.leavers / A.hc
ex = Exhibit(height=6.6)
ex.title([[("Hiring", ORANGE), (" fell to the ", INK), ("quit rate", NAVY), (",", INK)], [("so headcount went flat", INK)]])
ex.subtitle("Six largest Indian IT firms, % of headcount per year")
ex.legend([("Hires (implied)", ORANGE), ("Leavers (attrition)", NAVY)])
ex.source("Hires = net change + attrition × average headcount ÷ 4; firms' attrition definitions differ, and "
          "some count only voluntary exits. Quarters with at least five firms reporting. TCS's ~12,000 layoffs "
          "(Jul 2025–Mar 2026) fall in the post-period. Gap in 2021: too few firms report attrition.", "Source: Company fact sheets.", credit=CREDIT)
ax = ex.axes(left=0.11, right=0.86)
for s, col in [(l, NAVY), (h, ORANGE)]:
    gaps = s.index.to_series().diff() > pd.Timedelta(days=120)
    grp = gaps.cumsum().values
    for k in np.unique(grp):
        seg = s[grp == k]; ax.plot(seg.index, seg.values, color=col, lw=2.8)
    end_label(ax, s.index[-1], s.values[-1], f"{s.values[-1]:.0f}%", dy=7 if col == ORANGE else -7)
ax.set_ylim(0, 60); ax.set_yticks([0, 10, 20, 30, 40, 50]); ax.set_yticklabels(["0", "10", "20", "30", "40", "50%"])
year_axis(ax); ax.set_xlim(right=pd.Timestamp("2026-12-15")); post_line(ax, POST - pd.Timedelta(days=80), ymax=59.5)
finish(ex, ax, "05_hiring_pipeline")

# 06 · H6 revenue per employee: gap by firm and trend window ------------------------------
R6 = pd.read_csv("outputs/h6_rpe_gaps.csv").dropna(subset=["mean_gap_pct"])
firms = ["TCS", "Wipro", "Infosys", "HCLTech", "TechM"]
ex = Exhibit(height=6.0)
ex.title([[("No firm's revenue per", INK)], [("employee broke above trend", INK)]])
ex.subtitle("Average gap vs trend since 2024, %")
ex.legend([("Main (FY16–22)", ORANGE), ("Excl. 2021–22", NAVY), ("From 2019", GRAY)])
ex.source("Annualized US$ revenue ÷ average headcount, compared with each firm's log-linear trend. "
          "No firm is above its 95% band in the main version, and signs flip across trend windows. "
          "LTIMindtree excluded (history too short).", "Source: Company fact sheets.", credit=CREDIT)
ax = ex.axes(left=0.27, right=0.95, bottom_pad=0.5)
specs = [("main FY16-FY22", ORANGE, 0.0), ("excl. 2021-22 hiring boom", NAVY, 0.0), ("from 2019", GRAY, 0.0)]
for i, f in enumerate(firms):
    y = len(firms) - 1 - i; vals = []
    for spec, col, _ in specs:
        v = R6[(R6.firm == f) & (R6.spec == spec)].mean_gap_pct.iloc[0]; vals.append(v)
    ax.plot([min(vals), max(vals)], [y, y], color=GRID, lw=6, solid_capstyle="round", zorder=1)
    for (spec, col, _), v in zip(specs[::-1], vals[::-1]):
        ax.scatter([v], [y], s=130 if col == ORANGE else 95, color=col, edgecolor="white", lw=1.6, zorder=3)
    ax.text(-0.03, y, f, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=14.5, color=INK)
ax.axvline(0, color=INK, lw=1.2); ax.set_yticks([]); ax.set_ylim(-0.6, len(firms) - 0.4)
ax.set_xlim(-20, 25); ax.set_xticks([-15, -10, -5, 0, 5, 10, 15, 20]); ax.set_xticklabels(["−15", "−10", "−5", "0", "+5", "+10", "+15", "+20%"]); ax.tick_params(axis="x", labelsize=12.5)
ax.grid(axis="y", visible=False); ax.grid(axis="x", color=GRID, lw=1); ax.spines["bottom"].set_visible(False)
finish(ex, ax, "06_rev_per_employee")

# 07 · Decomposition ----------------------------------------------------------------------
D = pd.read_csv("outputs/h6_decomposition.csv")
ex = Exhibit(height=6.2)
ex.title([[("Revenue", ORANGE), (" growth slowed and", INK)], [("headcount", NAVY), (" stopped growing", INK)]])
ex.subtitle("TCS, Infosys, HCLTech and TechM combined, % per year")
ex.legend([("Revenue (US$)", ORANGE), ("Year-end headcount", NAVY)])
ex.source("Indian fiscal years (FY26 = Apr 2025–Mar 2026). Log growth. The gap between the bars is growth "
          "in revenue per employee.", "Source: Company fact sheets.", credit=CREDIT)
ax = ex.axes(left=0.11, right=0.97)
x = np.arange(len(D)); w = 0.38
ax.bar(x - w / 2, D.dlog_rev, w, color=ORANGE, zorder=2); ax.bar(x + w / 2, D.dlog_hc, w, color=NAVY, zorder=2)
ax.axhline(0, color=INK, lw=1.2, zorder=3)
ax.set_xticks(x); ax.set_xticklabels([f"'{str(f)[2:]}" for f in D.fy]); ax.set_ylim(-5, 30)
ax.set_yticks([0, 5, 10, 15, 20]); ax.set_yticklabels(["0", "5", "10", "15", "20%"]); ax.spines["bottom"].set_visible(False)
post_line(ax, list(D.fy).index(2024) - 0.5, label="AI coding tools\nspread (FY24)", ymax=29.5)
finish(ex, ax, "07_decomposition")

# 08 · H5 US IT services jobs -------------------------------------------------------------
b = pd.read_csv("data/processed/bls.csv", parse_dates=["date"])
g = b[b.series_id == "CES6054150001"].sort_values("date").reset_index(drop=True)
t = g.date.dt.year + (g.date.dt.month - 1) / 12
_, tr = loglin_trend(t, g.value, ((g.date >= "2015-01-01") & (g.date <= "2022-12-01")).values); g = pd.concat([g, tr], axis=1)
g = g[g.date >= "2015-01-01"]; gap = 100 * (g.value.iloc[-1] / g.trend.iloc[-1] - 1)
ex = Exhibit(height=6.4)
ex.title([[("US IT services jobs", ORANGE), (" are", INK)], [(f"{abs(gap):.0f}% below their ", INK), ("trend", NAVY)]])
ex.subtitle("Computer systems design & related services, millions")
ex.legend([("Actual", ORANGE), ("2015–22 trend", NAVY), ("95% band", LIGHT_N)])
ex.source("All employees, seasonally adjusted (NAICS 5415). Covers IT services firms in the US, not IT staff "
          "employed directly by other industries. Below the band every month since January 2024. Gap shown is Oct 2026; 2026 average: 13%.",
          "Source: BLS Current Employment Statistics (CES6054150001).", credit=CREDIT)
ax = ex.axes(left=0.12, right=0.86)
ax.fill_between(g.date, g.pi_lo / 1000, g.pi_hi / 1000, color=LIGHT_N, alpha=.6, lw=0, zorder=0)
ax.plot(g.date, g.trend / 1000, color=NAVY, lw=2, ls=(0, (4, 3)), zorder=2)
ax.plot(g.date, g.value / 1000, color=ORANGE, lw=2.8, zorder=3)
end_label(ax, g.date.iloc[-1], g.value.iloc[-1] / 1000, f"{g.value.iloc[-1]/1000:.2f}", dy=-4)
end_label(ax, g.date.iloc[-1], g.trend.iloc[-1] / 1000, f"{g.trend.iloc[-1]/1000:.2f}", color=NAVY, dy=4)
ax.set_ylim(1.8, 3.0); ax.set_yticks([1.8, 2.1, 2.4, 2.7, 3.0]); ax.set_yticklabels(["1.8", "2.1", "2.4", "2.7", "3.0m"])
year_axis(ax); ax.set_xlim(pd.Timestamp("2014-10-01"), pd.Timestamp("2026-12-15")); post_line(ax, POST - pd.Timedelta(days=80), ymax=2.98)
finish(ex, ax, "08_h5_us_it_jobs")
print("done")
