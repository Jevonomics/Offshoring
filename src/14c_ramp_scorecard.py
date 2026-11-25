"""Scorecard of the six tests as a Ramp-style table exhibit -> outputs/charts/ramp/00_scorecard.{png,svg}"""
import sys, textwrap
sys.path.insert(0, "src")
from exhibit import Exhibit, INK, SUB, GRID, ORANGE, NAVY, GRAY, MARGIN
from matplotlib.patches import Rectangle

VERDICT = {"Contrary": ORANGE, "No support": GRAY, "Support": NAVY}
SECTIONS = [
    ("Clients replacing vendors", [
        ("1", "Are US imports from India and the Philippines falling below trend?", "Contrary", "India 24% above trend in 2025"),
        ("2", "Did work exposed to AI shrink faster? (limited data)", "No support", "−0.4 points, p\u00a0=\u00a00.83"),
        ("3", "Did US clients pull back more than European ones?", "No support", "−3.8%, p\u00a0=\u00a00.65"),
        ("4", "Did headcount fall through hiring freezes rather than layoffs?", "Support", "All 20 declines outside TCS"),
        ("5", "Did US firms bring the work in-house?", "Contrary", "US IT jobs 13% below trend"),
    ]),
    ("Vendors' own productivity", [
        ("6", "Are vendors earning more per employee?", "No support", "0 of 5 firms above the band"),
    ]),
]
W = 7.6
ex = Exhibit(width=W, height=9.55)
ex.title([[("Five of six tests don't fit the story of", INK)], [("AI replacing offshore contractors", INK)]])
ex.subtitle("Verdicts on six tests set out before the data were collected")
ex.legend([(k, v) for k, v in VERDICT.items()])
ex.source("Contrary means the data moved the opposite way from the prediction. Test 4 matched, but hiring freezes "
          "are also how firms respond to an ordinary slowdown, so it doesn't point to AI in particular.",
          "Source: BEA, BLS, Accenture 8-K earnings releases, and Company fact sheets.", credit="Analysis: Atharv Joshi")
ax = ex.axes(left=MARGIN / W, right=1 - MARGIN / W, bottom_pad=0.15)
ax.axis("off")
pos = ax.get_position(); width_in, height_in = pos.width * W, pos.height * ex.h
ax.set_xlim(0, width_in); ax.set_ylim(height_in, 0)        # inches, y grows downward
X_NUM, X_Q, X_V, X_K = 0.0, 0.62, 3.95, 5.45
LINE = 0.25                                                 # inches per text line
FS = 13.5
def wrap(text, max_in):
    """Greedy wrap by rendered width (inches); never breaks inside a word or at hyphens."""
    probe = ex.fig.text(0, 0, "", fontsize=FS); out, cur = [], ""
    for w in text.split(" "):
        probe.set_text(f"{cur} {w}".strip())
        if cur and probe.get_window_extent(ex._r).width / ex.fig.dpi > max_in:
            out.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    probe.remove(); return out + [cur]
y = 0.15
for x, h in [(X_NUM, "Test"), (X_Q, "Question"), (X_V, "Verdict"), (X_K, "Key number")]:
    ax.text(x, y, h, fontsize=12, color=SUB, weight="semibold", va="baseline")
y += 0.22
ax.plot([0, width_in], [y, y], color=INK, lw=1.2)
for sec, rows in SECTIONS:
    y += 0.42
    ax.text(X_NUM, y, sec, fontsize=12.5, color=SUB, weight="semibold", va="baseline")
    y += 0.14
    for num, q, verdict, key in rows:
        ql = wrap(q, X_V - X_Q - 0.2); kl = wrap(key, width_in - X_K)
        n = max(len(ql), len(kl))
        top = y + 0.32
        ax.text(X_NUM, top, num, fontsize=13.5, color=SUB, va="baseline")
        for i, l in enumerate(ql):
            ax.text(X_Q, top + i * LINE, l, fontsize=13.5, color=INK, va="baseline")
        sq = 0.13
        ax.add_patch(Rectangle((X_V, top - sq * 0.95), sq, sq, color=VERDICT[verdict], lw=0))
        ax.text(X_V + sq + 0.08, top, verdict, fontsize=13.5, color=INK, weight="bold", va="baseline")
        for i, l in enumerate(kl):
            ax.text(X_K, top + i * LINE, l, fontsize=13.5, color=INK, va="baseline")
        y = top + (n - 1) * LINE + 0.17
        ax.plot([0, width_in], [y, y], color=GRID, lw=1)
ex.align_axes_ink(ax, x_to=pos.x0 + 0.3 / W)
ex.save("outputs/charts/ramp/00_scorecard")
print("bottom of table (in):", round(y, 2), "of", round(height_in, 2))
