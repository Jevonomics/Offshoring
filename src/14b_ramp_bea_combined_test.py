"""TEST: India and Philippines BEA charts side by side in one Ramp-style exhibit.
Output: outputs/charts/ramp/test_01_bea_combined.{png,svg}. The separate 01a/01b charts are unchanged."""
import sys
import pandas as pd
sys.path.insert(0, "src")
from exhibit import Exhibit, INK, SUB, ORANGE, NAVY, GRID, MARGIN
from analysis_common import loglin_trend

LIGHT_N = "#c3cde6"
B = pd.read_csv("data/processed/bea_imports.csv")
B = B[(B.affiliation == "AllAffiliations") & B.year.between(2015, 2025) & B.service_type.isin(["TelecomCompAndInfo", "OtherBusiness"])]

ex = Exhibit(width=11, height=6.4)
ex.title([[("US imports from ", INK), ("India", INK), (" ran above ", INK), ("trend", NAVY), ("; from the Philippines, below it", INK)]])
ex.subtitle("Computer & business services, US$ billions")
ex.legend([("Actual", ORANGE), ("2015–22 trend", NAVY), ("95% band", LIGHT_N)])
ex.source("India: above the 95% band in 2025 and further above trend than imports from all countries (+14%); on trend with a "
          "pre-COVID (2015–19) trend. Philippines: inside the band, the sign flips with other trend windows, and a 2022 BEA "
          "category change (call-center work moving to management consulting) likely affects 2022–25. Nominal US$.",
          "Source: BEA International Services (telecom, computer & information + other business services).",
          credit="Analysis: Atharv Joshi")
frame = ex.axes(left=0.05, right=0.95, bottom_pad=0.55)
_, y0, _, h = frame.get_position().bounds; frame.remove()
GUTTER, LABEL_ROOM = 0.7, 0.55                        # inches: between panels; right of each plot for end labels
slot_w = (ex.w - 2 * MARGIN - GUTTER) / 2
panels = [("India", (0, 45), [0, 10, 20, 30, 40], "+24%"), ("Philippines", (0, 12), [0, 3, 6, 9, 12], "−30%")]
axes = []
for i, (c, ylim, yt, gap) in enumerate(panels):
    slot_x0 = MARGIN + i * (slot_w + GUTTER)
    ax = ex.fig.add_axes([slot_x0 / ex.w, y0, (slot_w - LABEL_ROOM) / ex.w, h * 0.9])
    ax._slot_x0 = slot_x0 / ex.w
    ax.spines[["top", "right", "left"]].set_visible(False); ax.grid(axis="y", color=GRID, lw=1); ax.set_axisbelow(True)
    v = B[B.country == c].pivot_table(index="year", columns="service_type", values="value_usd_m")
    s = v.sum(axis=1).where(v.notna().all(axis=1)).dropna() / 1000
    _, tr = loglin_trend(s.index.values, s.values, s.index.values <= 2022); tr.index = s.index
    ax.fill_between(s.index, tr.pi_lo, tr.pi_hi, color=LIGHT_N, alpha=.6, lw=0, zorder=0)
    ax.plot(s.index, tr.trend, color=NAVY, lw=2, ls=(0, (4, 3)), zorder=2)
    ax.plot(s.index, s.values, color=ORANGE, lw=2.8, marker="o", ms=4.5, zorder=3)
    hi = s.values[-1] > tr.trend.values[-1]
    for val, col, dy in [(s.values[-1], INK, 6 if hi else -6), (tr.trend.values[-1], NAVY, -6 if hi else 6)]:
        ax.annotate(f"{val:.1f}", (2025, val), xytext=(6, dy), textcoords="offset points", va="center", fontsize=14, weight="bold", color=col)
    ax.set_ylim(*ylim); ax.set_yticks(yt); ax.set_yticklabels([str(t) for t in yt[:-1]] + [f"${yt[-1]}bn"])
    ax.set_xlim(2014.5, 2025.5); ax.set_xticks(range(2015, 2026)); ax.set_xticklabels([f"'{y % 100:02d}" for y in range(2015, 2026)])
    ax.tick_params(axis="x", labelsize=12); ax.tick_params(axis="y", labelsize=13)
    ax.axvline(2023.5, color=SUB, ls=(0, (3, 3)), lw=1.1, zorder=1)
    ax.annotate("AI coding tools\nspread (2024)", (2023.5, ylim[1] * 0.99), xytext=(-6, 0), textcoords="offset points",
                ha="right", va="top", color=SUB, fontsize=11.5, linespacing=1.15)
    # panel heading: country + 2025 gap, left-aligned with the panel's tick labels (aligned below)
    ax._heading = ex.fig.text(0, 0, "", fontsize=15, weight="bold")
    ax._heading.set_text(f"{c}  "); ax._gap = ex.fig.text(0, 0, f"{gap} vs trend in 2025", fontsize=13, color=SUB, weight="semibold")
    axes.append(ax)
# move each plot right so its tick labels start at its slot's left edge (the left slot = headline margin)
ex.fig.canvas.draw(); r = ex._r; W = ex.fig.bbox.width
for ax in axes:
    for _ in range(3):
        d = ax._slot_x0 - ax.get_tightbbox(r).x0 / W
        p = ax.get_position(); ax.set_position([p.x0 + d, p.y0, p.width - d, p.height]); ex.fig.canvas.draw()
    top = ax.get_position().y1 + 0.22 / ex.h
    ax._heading.set_position((ax._slot_x0, top)); ax._heading.set_va("baseline"); ex.fig.canvas.draw()
    ax._gap.set_position((ax._slot_x0 + ax._heading.get_window_extent(r).width / W, top)); ax._gap.set_va("baseline")
ex.save("outputs/charts/ramp/test_01_bea_combined")
print("done")
