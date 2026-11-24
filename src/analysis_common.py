"""Shared helpers: log-linear trend with prediction intervals; chart styling."""
import numpy as np, pandas as pd, statsmodels.api as sm, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
POST, POST_ROBUST = pd.Timestamp("2024-03-31"), pd.Timestamp("2023-03-31")  # first post-period quarter-ends (cal 2024Q1, 2023Q1)
CHATGPT = pd.Timestamp("2022-11-30")
def loglin_trend(t, y, fit_mask, alpha=0.05):
    """t: numeric time; y: positive values. Fit log(y)=a+b t on fit_mask; return frame with trend and PI for all t."""
    X = sm.add_constant(np.asarray(t, float)); m = sm.OLS(np.log(np.asarray(y, float)[fit_mask]), X[fit_mask]).fit()
    pr = m.get_prediction(X).summary_frame(alpha=alpha)
    return m, pd.DataFrame({"trend": np.exp(pr["mean"]), "pi_lo": np.exp(pr.obs_ci_lower), "pi_hi": np.exp(pr.obs_ci_upper)})
def style(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color="#e5e5e5", lw=.6)
def mark_periods(ax, x_is_date=True):
    ax.axvline(CHATGPT, color="#888", lw=.8, ls=":"); ax.axvspan(POST - pd.Timedelta(days=80), ax.get_xlim()[1] if not x_is_date else pd.Timestamp("2026-12-31"), color="#f0f0f0", zorder=0)
def save(fig, name):
    for ext in ("png", "svg"): fig.savefig(f"outputs/charts/{name}.{ext}", dpi=160, bbox_inches="tight")
    plt.close(fig)
