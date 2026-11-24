"""Shared helpers for vendor extraction: Indian fiscal quarter -> calendar quarter end; long-format writer."""
import os, pandas as pd
QEND = {1: "06-30", 2: "09-30", 3: "12-31", 4: "03-31"}
def fy_q_to_cal(fy: int, q: int) -> str:
    """Indian FY (Apr-Mar). FY2027 Q1 = Apr-Jun 2026 -> '2026-06-30'. fy is 4-digit."""
    year = fy - 1 if q in (1, 2, 3) else fy
    return f"{year}-{QEND[q]}"
LONG_COLS = ["firm", "fiscal_label", "cal_quarter_end", "section", "variable", "value", "unit", "basis", "source_file", "locator"]
def write_long(rows, firm):
    df = pd.DataFrame(rows, columns=LONG_COLS)
    os.makedirs("data/interim", exist_ok=True)
    df.to_csv(f"data/interim/vendor_long_{firm}.csv", index=False)
    return df
