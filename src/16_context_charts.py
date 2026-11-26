"""Context charts (not tests): stock prices, raw headcount, raw revenue growth -> outputs/charts/ramp/09-12."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "src")
from exhibit import Exhibit, INK, SUB, GRID, ORANGE, NAVY, GRAY, MARGIN
import matplotlib.dates as mdates

OUT, CREDIT = "outputs/charts/ramp/", "Analysis: Atharv Joshi"
F = ["TCS", "Infosys", "HCLTech", "Wipro", "TechM", "LTIMindtree"]
AI_DAYS = ["2026-02-04", "2026-02-12", "2026-02-24", "2026-04-10", "2026-10-27"]


def align_left(ex, ax, iters=4):
    for _ in range(iters):
        ex.fig.canvas.draw()
        d = MARGIN / ex.w - ax.get_tightbbox(ex._r).x0 / ex.fig.bbox.width
        if abs(d) < 2e-4: break
        p = ax.get_position(); ax.set_position([p.x0 + d, p.y0, p.width - d, p.height])


def year_axis(ax, fmt="'%y", step=1):
    ax.xaxis.set_major_locator(mdates.YearLocator(step)); ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    ax.tick_params(axis="x", labelsize=12.5)


P = pd.read_csv("data/processed/stock_prices.csv", parse_dates=["date"]).pivot_table(index="date", columns="name", values="adjclose").ffill()

# 09 · Nifty IT vs Nifty 50 -------------------------------------------------------------------
r = np.log(P).diff(); rel = (r["Nifty IT"] - r["Nifty 50"]) * 100
ytd, on_ai = rel.loc["2026"].sum(), rel.loc[AI_DAYS].sum()
S = P.loc["2023-01-01":, ["Nifty IT", "Nifty 50"]]; S = S / S.iloc[0] * 100
ex = Exhibit(height=6.9)
ex.title([[("Indian IT stocks", ORANGE), (" fell behind the", INK)], [("market", NAVY), (" on days of AI news", INK)]])
ex.subtitle("Price index, Jan 2, 2023 = 100")
ex.legend([("Nifty IT", ORANGE), ("Nifty 50", NAVY), ("Days with Anthropic news", INK)])
ex.source(f"In 2026, Nifty IT has trailed the Nifty 50 by {abs(ytd):.0f} log points. The five marked days account for "
          f"{abs(on_ai):.0f} of them, so all other days together were slightly positive. Press reports tied each "
          "marked day to an Anthropic release or filing; on Feb 12, US jobs data also weighed. Other big drops had other "
          "causes, such as Infosys's weak guidance on Apr 24. Prices show what investors expect, not what has happened.",
          "Source: NSE indices via Yahoo Finance; press reports.", credit=CREDIT)
ax = ex.axes(left=0.1, right=0.86)
ax.plot(S.index, S["Nifty 50"], color=NAVY, lw=2)
ax.plot(S.index, S["Nifty IT"], color=ORANGE, lw=2)
d = pd.to_datetime(AI_DAYS); ax.scatter(d, S["Nifty IT"].loc[d], s=34, color=INK, zorder=4, edgecolor="white", lw=1)
for col, c in [("Nifty IT", ORANGE), ("Nifty 50", NAVY)]:
    ax.annotate(f"{S[col].iloc[-1]:.0f}", (S.index[-1], S[col].iloc[-1]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=15, weight="bold", color=c)
ax.set_ylim(80, 160); ax.set_yticks(range(80, 161, 20)); year_axis(ax, "%Y")
ax.set_xlim(pd.Timestamp("2022-12-20"), pd.Timestamp("2026-12-31"))
align_left(ex, ax); ex.align_axes_ink(ax); ex.save(OUT + "09_stocks_vs_market")
print(f"09: YTD {ytd:.1f}, AI days {on_ai:.1f}")

# 10 · each firm vs its home index, since Jan 2024 -----------------------------------------------
home = {f: "Nifty 50" for f in F}; home["Accenture"] = "S&P 500"
s24 = P.loc["2024-01-01":]
T = pd.Series({f: ((s24[f].iloc[-1] / s24[f].iloc[0]) / (s24[home[f]].iloc[-1] / s24[home[f]].iloc[0]) - 1) * 100
               for f in home}).sort_values(ascending=False)
n_trail = int((T < 0).sum())
ex = Exhibit(height=6.6)
W2 = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven"}
ex.title([[(f"{W2[n_trail]} of {W2[len(T)].lower()} firms trail their", INK)], [("home market since 2024", INK)]])
ex.subtitle("Share price relative to home index since Jan 2, 2024, %")
ex.legend([("Indian firms vs Nifty 50", ORANGE), ("Accenture vs S&P 500", NAVY)])
ex.source("Total returns (prices adjusted for dividends and splits), to Nov 25, 2026. Relative return = (1 + firm return) "
          "÷ (1 + index return) − 1, so −50% means the firm is worth half as much relative to its market as in January 2024.",
          "Source: NSE and NYSE prices via Yahoo Finance.", credit=CREDIT)
ax = ex.axes(left=0.25, right=0.9, bottom_pad=0.5)
ax.grid(axis="y", visible=False); ax.grid(axis="x", color=GRID, lw=1); ax.spines["bottom"].set_visible(False)
y = np.arange(len(T))[::-1]
ax.barh(y, T.values, height=0.62, color=[NAVY if f == "Accenture" else ORANGE for f in T.index], zorder=2)
for yi, v in zip(y, T.values):
    ax.annotate(f"{v:+.0f}%".replace("-", "−"), (v, yi), xytext=(6 if v >= 0 else -6, 0), textcoords="offset points",
                ha="left" if v >= 0 else "right", va="center", fontsize=13.5, weight="bold", color=INK)
ax.axvline(0, color=INK, lw=1.4, zorder=3)
ax.set_yticks(y); ax.set_yticklabels(T.index, fontsize=14.5, color=INK); ax.tick_params(axis="y", pad=12)
ax.set_xlim(-75, 45); ax.set_xticks(range(-60, 41, 20))
ax.set_xticklabels([f"{x:+d}".replace("-", "−") if x else "0" for x in range(-60, 41, 20)])
ax.set_ylim(-0.6, len(T) - 0.4)
align_left(ex, ax); ex.align_axes_ink(ax); ex.save(OUT + "10_stocks_by_firm")
print("10:", T.round(1).to_dict())

# 11 & 12 · small multiples ---------------------------------------------------------------------
V = pd.read_csv("data/processed/vendor_panel.csv", parse_dates=["cal_quarter_end"])
H = V.pivot_table(index="cal_quarter_end", columns="firm", values="headcount_total")[F] / 1000
R = V.pivot_table(index="cal_quarter_end", columns="firm", values="revenue_usd_m")[F]
R4 = R.rolling(4, min_periods=4).sum(); G = (R4 / R4.shift(4) - 1) * 100

def grid(ex, draw, name, ncols=2):
    """2 x 3 panels inside the space ex.axes() would use; headings sit on each column's label edge."""
    base = ex.axes(left=0.1, right=0.97, bottom_pad=0.4); p = base.get_position(); base.remove()
    nrows = int(np.ceil(len(F) / ncols)); hgap, vgap = 1.05 / ex.w, 0.85 / ex.h
    w = (p.width - (ncols - 1) * hgap) / ncols; h = (p.height - (nrows - 1) * vgap - 0.3 / ex.h) / nrows
    axes = []
    for k, f in enumerate(F):
        rr, cc = divmod(k, ncols)
        ax = ex.fig.add_axes([p.x0 + cc * (w + hgap), p.y1 - 0.3 / ex.h - (rr + 1) * h - rr * vgap, w, h])
        ax.spines[["top", "right", "left"]].set_visible(False); ax.grid(axis="y", color=GRID, lw=1); ax.set_axisbelow(True)
        ax.tick_params(labelsize=11.5); draw(ax, f); axes.append(ax)
    W = ex.fig.bbox.width
    for _ in range(4):   # fit ink between the margins: shift for the left labels, squeeze for the right ones
        ex.fig.canvas.draw()
        L = min(a.get_tightbbox(ex._r).x0 for a in axes[::ncols]) / W
        Rr = max(a.get_tightbbox(ex._r).x1 for a in axes[ncols - 1::ncols]) / W
        lo, hi = MARGIN / ex.w, 1 - MARGIN / ex.w
        if abs(L - lo) < 2e-4 and Rr <= hi + 2e-4: break
        k = min(1.0, (hi - lo) / (Rr - L))
        for a in axes:
            q = a.get_position()
            a.set_position([lo + (q.x0 - L) * k, q.y0, q.width * k, q.height])
    ex.fig.canvas.draw()
    for c in range(ncols):
        col = axes[c::ncols]; x0 = min(a.get_tightbbox(ex._r).x0 for a in col) / W
        for a, f in zip(col, F[c::ncols]):
            ex.fig.text(x0 - ex._lsb(f, 13, weight="bold"), a.get_position().y1 + 0.17 / ex.h, f, fontsize=13,
                        weight="bold", color=INK, va="baseline")
    ex.save(OUT + name)

def draw_h(ax, f):
    s = H[f].loc[H[f].first_valid_index():].loc["2015":]
    if f == "TCS": ax.axvspan(pd.Timestamp("2025-07-01"), pd.Timestamp("2026-03-31"), color=GRAY, alpha=.35, lw=0)
    ax.plot(s.index, s, color=NAVY, lw=2)
    ax.scatter(s.idxmax(), s.max(), s=22, color=INK, zorder=3)
    lo, hi = s.min(), s.max(); pad = (hi - lo) * 0.12
    ax.set_ylim(max(0, lo - pad), hi + pad)
    ax.set_xlim(pd.Timestamp("2015-01-01"), pd.Timestamp("2026-12-31"))
    ax.xaxis.set_major_locator(mdates.YearLocator(3)); ax.xaxis.set_major_formatter(mdates.DateFormatter("'%y"))
    ax.yaxis.set_major_locator(__import__("matplotlib").ticker.MaxNLocator(4))
    ax.yaxis.set_major_formatter(__import__("matplotlib").ticker.FuncFormatter(lambda v, _: f"{v:.0f}k"))

ex = Exhibit(height=9.1)
ex.title([[("Four of six firms employ fewer", INK)], [("people than at their 2022 peak", INK)]])
ex.subtitle("Total headcount at quarter end, thousands")
ex.legend([("Headcount", NAVY), ("Peak", INK), ("TCS layoff period", GRAY)])
ex.source("Reported headcount is net of all exits, so it includes layoffs. TCS lost 31,000 people from Jun to Dec "
          "2025, more than the 12,261 layoffs it announced, then regained 16,000. Each panel has its own scale. "
          "LTIMindtree begins at its 2021 restated figures; earlier figures cover LTI alone and aren't comparable.",
          "Source: Company fact sheets.", credit=CREDIT)
grid(ex, draw_h, "11_headcount_by_firm")

def draw_g(ax, f):
    s = G[f].loc[G[f].first_valid_index():].loc["2016":]
    ax.axhline(0, color=INK, lw=1.2)
    ax.plot(s.index, s, color=ORANGE, lw=2)
    s = s.loc[:s.last_valid_index()]
    ax.annotate(f"{s.iloc[-1]:.1f}%".replace("-", "−"), (s.index[-1], s.iloc[-1]), xytext=(5, 0),
                textcoords="offset points", va="center", fontsize=11.5, weight="bold", color=ORANGE)
    ax.set_ylim(-10, 25); ax.set_yticks([-10, 0, 10, 20])
    ax.set_yticklabels(["−10", "0", "10", "20%"])
    ax.set_xlim(pd.Timestamp("2016-01-01"), pd.Timestamp("2027-06-30"))
    ax.xaxis.set_major_locator(mdates.YearLocator(3)); ax.xaxis.set_major_formatter(mdates.DateFormatter("'%y"))

lo, hi = G.iloc[-1].min(), G.iloc[-1].max()
ex = Exhibit(height=9.1)
ex.title([[("Revenue", ORANGE), (" is growing just ", INK), (f"{lo:.0f}–{hi:.0f}%", INK)], [("a year at every firm", INK)]])
ex.subtitle("US$ revenue, last four quarters vs the four before, %")
ex.legend([("Revenue growth", ORANGE)])
ex.source("Before COVID (2016–19), annual growth averaged about 8% at TCS, Infosys, and Tech Mahindra, 11% at HCLTech, "
          "and 3% at Wipro. US$ figures move with exchange rates. Gaps are quarters with missing data. LTIMindtree "
          "begins in 2022 (restated history starts in 2021).",
          "Source: Company fact sheets.", credit=CREDIT)
grid(ex, draw_g, "12_revenue_growth_by_firm")
print("done")

# 13 · per firm: share price vs Nifty 50, revenue, and headcount, indexed to end-2023 --------------
BASE = pd.Timestamp("2023-12-31")
REL = P[F].div(P["Nifty 50"], axis=0).resample("W-FRI").last()
REL = REL / REL.loc[:BASE].iloc[-1] * 100
RI = R4 / R4.loc[BASE] * 100
HI = (H * 1000) / (H.loc[BASE] * 1000) * 100
HC_COLOR = "#9a9994"

def draw_all(ax, f):
    ax.axhline(100, color=INK, lw=1.1, zorder=1)
    for s, c, lw in [(HI[f], HC_COLOR, 2), (RI[f], NAVY, 2), (REL[f], ORANGE, 2)]:
        s = s.loc["2022-01-01":]; ax.plot(s.index, s, color=c, lw=lw, zorder=3)
    e = REL[f].dropna()
    ax.annotate(f"{e.iloc[-1]:.0f}", (e.index[-1], e.iloc[-1]), xytext=(5, 0), textcoords="offset points",
                va="center", fontsize=11.5, weight="bold", color=ORANGE)
    ax.set_ylim(40, 190); ax.set_yticks([50, 100, 150])
    ax.set_xlim(pd.Timestamp("2022-01-01"), pd.Timestamp("2027-02-15"))
    ax.set_xticks([pd.Timestamp(f"{y}-07-01") for y in range(2022, 2027)])
    ax.set_xticklabels([f"'{y % 100}" for y in range(2022, 2027)])
    ax.spines["bottom"].set_visible(False)

n_fell = int((REL.iloc[-1] < 100).sum())
W2 = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
ex = Exhibit(height=9.1)
ex.title([[(f"{W2[n_fell]} of six firms' ", INK), ("shares fell", ORANGE), (" while", INK)],
          [("revenue", NAVY), (" and ", INK), ("headcount", HC_COLOR), (" held steady", INK)]])
ex.subtitle("Index, Dec 31, 2023 = 100")
ex.legend([("Share price vs Nifty 50", ORANGE), ("Revenue", NAVY), ("Headcount", HC_COLOR)])
ex.source("Share price is relative to the Nifty 50 (weekly, to Nov 25, 2026; labeled at the end). Revenue is US$, "
          "summed over the last four quarters. Headcount is at quarter end, net of all exits. Company data run to "
          "Sep 30, 2026. LTIMindtree uses its restated combined figures.",
          "Source: Company fact sheets; NSE prices via Yahoo Finance.", credit=CREDIT)
grid(ex, draw_all, "13_price_revenue_headcount")
print("13 done")
