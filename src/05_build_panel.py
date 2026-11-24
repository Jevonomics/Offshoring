"""Combine vendor long files -> data/processed/vendor_panel.csv (wide, firm x quarter),
data/processed/vendor_segments.csv (long shares + implied revenue), vendor rows in provenance.csv,
and outputs/validation.md (runbook Step 3 checks)."""
import glob, numpy as pd_np, numpy as np, pandas as pd
L = pd.concat([pd.read_csv(f) for f in glob.glob("data/interim/vendor_long_*.csv")], ignore_index=True)
L["firm"] = L.firm.replace({"LTI": "LTI (standalone)"})
# Shares: normalize to percent
pct_share = L.variable.str.startswith("rev_share") | L.variable.str.startswith("attrition") | L.variable.str.startswith("utilization")
L.loc[pct_share & (L.unit == "share"), "value"] *= 100
L.loc[pct_share, "unit"] = "pct"
# ---- wide panel
core = {"revenue_usd_m": "revenue_usd_m", "revenue_it_usd_m": "revenue_usd_m", "headcount_total": "headcount_total",
        "net_addition": "net_addition", "gross_hires": "gross_hires", "fresher_hires": "fresher_hires",
        "utilization_excl_trainees": "utilization_excl_trainees", "subcontracting_cost_usd_m": "subcontracting_cost_usd_m",
        "headcount_bps": "headcount_bps", "headcount_software": "headcount_software"}
W = L[L.variable.isin(core)].assign(col=lambda d: d.variable.map(core))
att = L[L.variable.str.startswith("attrition")].copy()
att["col"] = "attrition_pct"; att["attrition_definition"] = att.variable
W = pd.concat([W, att])
panel = W.pivot_table(index=["firm", "cal_quarter_end", "fiscal_label"], columns="col", values="value", aggfunc="first").reset_index()
# attrition: one definition per firm-quarter (prefer the IT/LTM definition); keep the label
pref = ["attrition_ltm_it", "attrition_ltm_it_voluntary", "attrition_ltm", "attrition_ltm_it_voluntary",
        "attrition[Voluntary Attrition % (LTM - IT Services)]", "attrition[Voluntary Attrition % (Annualized - IT Services)]",
        "attrition[Attrition % (Annualized Consolidated)]", "attrition[Attrition % (LTM)*]"]
a = att.assign(rank=att.variable.map({v: i for i, v in enumerate(pref)}).fillna(99)).sort_values("rank").drop_duplicates(["firm", "cal_quarter_end"])
panel = panel.drop(columns="attrition_pct", errors="ignore").merge(a[["firm", "cal_quarter_end", "value", "variable"]].rename(
    columns={"value": "attrition_pct", "variable": "attrition_definition"}), on=["firm", "cal_quarter_end"], how="left")
# North America / Americas share (H3): firm-specific definition recorded
reg = L[L.variable.str.startswith("rev_share_region") | L.variable.str.startswith("rev_share_mix")].copy()
reg["label"] = reg.variable.str.split(":").str[1]
def na_share(g):
    lab = dict(zip(g.label, g.value))
    for k, d in [("North America", "North America"), ("USA", "USA"), ("Americas", "Americas")]:
        if k in lab: return pd.Series({"na_share_pct": lab[k], "na_definition": d, "europe_share_pct": lab.get("Europe [svc]" if k == "USA" else "Europe", np.nan)})
    if "Americas 1" in lab and "Americas 2" in lab:
        return pd.Series({"na_share_pct": lab["Americas 1"] + lab["Americas 2"], "na_definition": "Americas 1+2 (SMU)", "europe_share_pct": lab.get("Europe", np.nan)})
    return pd.Series({"na_share_pct": np.nan, "na_definition": None, "europe_share_pct": lab.get("Europe", np.nan)})
# HCLTech: prefer Americas while reported (consistent basis), USA only after Americas ends
r2 = reg.copy()
hcl_am = set(r2[(r2.firm == "HCLTech") & (r2.label == "Americas")].cal_quarter_end)
r2 = r2[~((r2.firm == "HCLTech") & (r2.label == "USA") & r2.cal_quarter_end.isin(hcl_am))]
nas = r2.groupby(["firm", "cal_quarter_end"]).apply(na_share, include_groups=False).reset_index()
panel = panel.merge(nas, on=["firm", "cal_quarter_end"], how="left")
panel = panel.sort_values(["firm", "cal_quarter_end"])
panel.to_csv("data/processed/vendor_panel.csv", index=False)
# ---- segments (long) with implied revenue
seg = L[L.variable.str.startswith("rev_share")].copy()
seg["segment_type"] = np.where(seg.variable.str.contains("region"), "region", np.where(seg.variable.str.contains("service_line"), "service_line", "mix"))
seg.loc[(seg.firm == "HCLTech") & seg.variable.str.contains(r"Americas|USA|Europe|RoW|ROW|India"), "segment_type"] = "region"
seg.loc[(seg.firm == "HCLTech") & (seg.segment_type == "mix"), "segment_type"] = "service_line"
seg["segment_label"] = seg.variable.str.split(":").str[1]
rev = panel.set_index(["firm", "cal_quarter_end"]).revenue_usd_m
seg["implied_revenue_usd_m"] = seg.value / 100 * seg.set_index(["firm", "cal_quarter_end"]).index.map(rev).values
seg.rename(columns={"value": "share_pct"})[["firm", "cal_quarter_end", "fiscal_label", "segment_type", "segment_label", "share_pct", "implied_revenue_usd_m", "source_file"]] \
   .to_csv("data/processed/vendor_segments.csv", index=False)
# ---- provenance
prov = pd.DataFrame(dict(source_id=L.firm.str.lower().str.replace(r"[^a-z]", "", regex=True) + "_" + L.fiscal_label, entity=L.firm,
    period=L.fiscal_label, variable=L.variable, value=L.value, unit=L.unit, basis=L.basis, source_url=L.source_file,
    page_or_table=L.locator, extracted_by="script", notes=""))
p = "data/processed/provenance.csv"; old = pd.read_csv(p)
pd.concat([old[old.source_id.str.startswith("bea_")], prov]).to_csv(p, index=False)
print(panel.groupby("firm").agg(first=("cal_quarter_end", "min"), last=("cal_quarter_end", "max"), n=("cal_quarter_end", "size"),
      rev=("revenue_usd_m", "count"), hc=("headcount_total", "count"), na=("na_share_pct", "count")).to_string())
