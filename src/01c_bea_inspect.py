"""Summarize BEA raw pulls: availability by country x type x affiliation x year."""
import json, glob, pandas as pd
rows = []
for fn in glob.glob("data/raw/bea/imports_*.json"):
    d = json.load(open(fn))
    for r in d["BEAAPI"]["Results"]["Data"]:
        rows.append(r)
df = pd.DataFrame(rows).drop_duplicates()
print(df.columns.tolist()); print(df.head(3).to_string())
df["num"] = pd.to_numeric(df["DataValue"].str.replace(",", ""), errors="coerce")
key = ["TypeOfService", "Affiliation"]
types = ["AllTypesOfService","TelecomCompAndInfo","Comp","OtherBusiness","ProfMgmtConsult","BusMgmtConsPubRel","Legal",
         "AccountAuditBookkeep","ResearchAndDev","TechTradeRelatedOth","OthBusinessNie","PotIctEnServ","IctServ"]
for c in ["India","Philippines","AllCountries"]:
    s = df[(df.AreaOrCountry==c) & df.TypeOfService.isin(types)]
    g = s.groupby(key).agg(first=("Year","min"), last=("Year","max"), n=("num", lambda x: x.notna().sum()), nobs=("Year","count")).reset_index()
    print(f"\n=== {c}"); print(g.to_string(index=False))
