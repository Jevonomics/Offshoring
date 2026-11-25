"""Adapted from Jevonomics/Ramp-AI-Index exhibit.py.

Exhibit layout in the style of Ramp Economics Lab charts: off-white background, large bold
headline (key words can take a series color), bold gray subtitle, square-swatch legend,
light horizontal grid, gray tick labels, source line at the bottom left.

    ex = Exhibit(height=6.4)
    ex.title([[("Ramp", ORANGE), ("'s rate is", INK)], [("more than double", INK)]])
    ex.subtitle("Share of U.S. businesses using AI, %")
    ex.legend([("Ramp", ORANGE), ("Census", NAVY)])
    ax = ex.axes(left=0.12, right=0.92)
    ...
    ex.source("Source: ...")
    ex.save("charts/name")

Fonts: Inter (SIL Open Font License), bundled in fonts/.
"""
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle
from matplotlib.transforms import ScaledTranslation
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
import numpy as np

for f in glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", "*.ttf")):
    font_manager.fontManager.addfont(f)

BG, INK, SUB, TICK = "#fbfaf7", "#1c1c1a", "#6f6e6a", "#8f8e8a"
GRID, BASE = "#dddbd6", "#3a3a38"
ORANGE, NAVY, GRAY = "#e0702f", "#3f5ea6", "#b3b2ad"   # orange/navy validated as a pair

plt.rcParams.update({
    "font.family": "Inter", "font.size": 13, "text.color": INK,
    "axes.facecolor": BG, "figure.facecolor": BG, "savefig.facecolor": BG,
    "axes.edgecolor": BASE, "axes.linewidth": 1.2,
    "xtick.color": TICK, "ytick.color": TICK, "xtick.labelsize": 14, "ytick.labelsize": 14,
    "xtick.major.size": 0, "ytick.major.size": 0, "xtick.major.pad": 8, "ytick.major.pad": 8,
    "svg.fonttype": "path",   # embed glyph outlines so SVGs look the same without Inter
})

MARGIN = 0.32  # inches, left/right page margin
CAP = 0.727    # Inter cap height, as a fraction of font size
DPI = 200


class Exhibit:
    def __init__(self, width=6.2, height=6.4):
        # Measure text at the output resolution, or headline pieces drift apart.
        self.fig = plt.figure(figsize=(width, height), dpi=DPI)
        self.w, self.h = width, height
        self.cursor = 0.30            # inches from the top for the next header element
        self.footer = 0.0             # inches reserved at the bottom by source lines
        self._r = self.fig.canvas.get_renderer()

    # header ------------------------------------------------------------------
    def _y(self):
        return 1 - self.cursor / self.h

    def _lsb(self, text, size, family="Inter", weight="normal"):
        """Blank space before the first glyph's ink, as a figure fraction, so text can start its
        ink exactly on the margin like the legend swatches do."""
        if not text.strip():
            return 0.0
        ext = TextPath((0, 0), text.lstrip(), size=size, prop=FontProperties(family=family, weight=weight)).get_extents()
        return ext.x0 / 72 / self.w

    def _width(self, t):
        return t.get_window_extent(self._r).width / self.fig.bbox.width

    def title(self, lines, size=23):
        """lines: list of lines, each a list of (text, color) pieces."""
        for line in lines:
            x = MARGIN / self.w - self._lsb(line[0][0], size, "Inter Display", "bold")
            for text, color in line:
                t = self.fig.text(x, self._y(), text, color=color, fontsize=size,
                                  family="Inter Display", weight="bold", va="top")
                x += self._width(t)
            self.cursor += size * 1.18 / 72
        self.cursor += 0.16

    def subtitle(self, text, size=12.5):
        self.fig.text(MARGIN / self.w - self._lsb(text, size, weight="semibold"), self._y(), text,
                      color=SUB, fontsize=size, weight="semibold", va="top")
        self.cursor += size * 1.3 / 72 + 0.2

    def legend(self, items, size=13):
        """items: (label, color) pairs, laid out in one row with square swatches."""
        x, side = MARGIN / self.w, size * 0.8 / 72
        baseline = self._y() - size * CAP / 72 / self.h
        mid = baseline + size * CAP / 2 / 72 / self.h     # swatch centered on the cap height
        for label, color in items:
            self.fig.add_artist(Rectangle((x, mid - side / 2 / self.h), side / self.w,
                                          side / self.h, color=color,
                                          transform=self.fig.transFigure))
            t = self.fig.text(x + (side + 0.07) / self.w, baseline, label, fontsize=size,
                              va="baseline", color=INK)
            x += (side + 0.07) / self.w + self._width(t) + 0.17 / self.w
        self.cursor += size * 1.3 / 72 + 0.3

    # body and footer ---------------------------------------------------------
    def _wrap(self, text, size, avail):
        """Split text into lines no wider than `avail` (figure fraction)."""
        probe = self.fig.text(0, 0, "", fontsize=size)
        lines, cur = [], ""
        for word in text.split():
            probe.set_text(f"{cur} {word}".strip())
            if cur and self._width(probe) > avail:
                lines.append(cur)
                cur = word
            else:
                cur = f"{cur} {word}".strip()
        probe.remove()
        return lines + [cur]

    def source(self, *paragraphs, size=9.5, credit=None, gap=0.55):
        """Notes and source at the bottom left, first paragraph on top, with a small gap between
        paragraphs. Text uses the full width; only the bottom line, which shares the baseline with
        `credit` (bottom-right corner), wraps short of it."""
        full = 1 - 2 * MARGIN / self.w
        short = full
        if credit:
            t = self.fig.text(1 - MARGIN / self.w, 0.22 / self.h, credit, fontsize=11,
                              weight="semibold", color=INK, ha="right", va="bottom")
            short -= self._width(t) + 0.3 / self.w
        blocks = [self._wrap(p, size, full) for p in paragraphs]
        probe = self.fig.text(0, 0, blocks[-1][-1], fontsize=size)
        if self._width(probe) > short:          # bottom line would run into the credit
            blocks[-1] = blocks[-1][:-1] + self._wrap(blocks[-1][-1], size, short)
        probe.remove()
        y, step = 0.22, size * 1.35 / 72
        for bi, block in enumerate(reversed(blocks)):
            if bi:
                y += step * gap
            for line in reversed(block):
                self.fig.text(MARGIN / self.w - self._lsb(line, size), y / self.h, line, color=SUB,
                              fontsize=size, va="bottom")
                y += step
        self.footer = y + 0.25

    def axes(self, left=0.1, right=0.95, bottom_pad=0.55):
        """Axes filling the space between the header and the footer reserve (set source()
        first). bottom_pad: inches for x tick labels."""
        top = self._y() - 0.1 / self.h
        bottom = (self.footer + bottom_pad) / self.h
        ax = self.fig.add_axes([left, bottom, right - left, top - bottom])
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="y", color=GRID, lw=1)
        ax.set_axisbelow(True)
        return ax

    def ink_left(self, y0, y1, x_from=0.0, x_to=1.0):
        """Leftmost inked pixel column (figure fraction) within a horizontal band (figure fractions)."""
        self.fig.canvas.draw()
        img = np.asarray(self.fig.canvas.buffer_rgba())[..., :3].astype(float) / 255
        H, W = img.shape[:2]
        bg = np.array(matplotlib.colors.to_rgb(BG))
        band = img[int(H * (1 - y1)):int(H * (1 - y0)), int(W * x_from):int(W * x_to)]
        cols = np.where((np.abs(band - bg).sum(axis=2) > 0.25).any(axis=0))[0]
        return (cols.min() + int(W * x_from)) / W if len(cols) else None

    def align_axes_ink(self, ax, x_target=None, x_from=0.0, x_to=None, iters=4):
        """Shift `ax` (left edge only) until its leftmost visible ink sits on x_target (default: margin)."""
        x_target = MARGIN / self.w if x_target is None else x_target
        for _ in range(iters):
            p = ax.get_position()
            bb = ax.get_tightbbox(self._r).transformed(self.fig.transFigure.inverted())
            left = self.ink_left(bb.y0, bb.y1, x_from, x_to if x_to is not None else p.x0 + 0.02)
            if left is None:
                break
            d = x_target - left
            if abs(d) < 0.5 / self.fig.bbox.width:
                break
            ax.set_position([p.x0 + d, p.y0, p.width - d, p.height])

    def save(self, path):
        # Center y tick labels on their gridlines: baseline-aligned, then shifted down by
        # half the cap height (matplotlib's own centering includes the descender).
        for ax in self.fig.axes:
            for lab in ax.get_yticklabels():
                shift = ScaledTranslation(0, -lab.get_fontsize() * CAP / 2 / 72,
                                          self.fig.dpi_scale_trans)
                lab.set_verticalalignment("baseline")
                lab.set_transform(lab.get_transform() + shift)
        for ext in ("png", "svg"):
            self.fig.savefig(f"{path}.{ext}", dpi=DPI)
        plt.close(self.fig)
