"""Build data/processed/bea_imports.csv (year x country x service_type x affiliation x value_usd_m)
and append BEA rows to data/processed/provenance.csv. Suppressed values ('(D)', 'n.a.', '(*)') -> NA."""
import glob, json, os, pandas as pd
rows = []
for fn in sorted(glob.glob("data/raw/bea/imports_*.json")):
    for r in json.load(open(fn))["BEAAPI"]["Results"]["Data"]:
        rows.append(dict(year=int(r["Year"]), country=r["AreaOrCountry"], service_type=r["TypeOfService"],
                         service_desc=r["TimeSeriesDescription"].split(";")[0].replace("Imports of ", ""),
                         affiliation=r["Affiliation"], raw=r["DataValue"], unit_mult=r["UNIT_MULT"],
                         series_id=r["TimeSeriesId"], note=r.get("NoteRef", ""), src=os.path.basename(fn)))
df = pd.DataFrame(rows).drop_duplicates(subset=["year", "country", "service_type", "affiliation"])
assert (df.unit_mult.astype(str) == "6").all(), "unexpected unit multiplier"
df["value_usd_m"] = pd.to_numeric(df.raw.str.replace(",", ""), errors="coerce")
df["suppressed"] = df.value_usd_m.isna()
os.makedirs("data/processed", exist_ok=True)
out = df[["year", "country", "service_type", "service_desc", "affiliation", "value_usd_m", "suppressed", "raw", "series_id"]]
out.sort_values(["country", "service_type", "affiliation", "year"]).to_csv("data/processed/bea_imports.csv", index=False)
prov = pd.DataFrame(dict(source_id="bea_intlservtrade_" + df.series_id, entity=df.country, period=df.year.astype(str),
    variable="imports_" + df.service_type + "_" + df.affiliation, value=df.value_usd_m, unit="USD_m", basis="nominal",
    source_url="https://apps.bea.gov/api/data?method=GetData&DatasetName=IntlServTrade&TradeDirection=Imports",
    page_or_table="IntlServTrade " + df.series_id, extracted_by="script",
    notes=df.apply(lambda r: f"suppressed: {r.raw}" if r.suppressed else "", axis=1)))
p = "data/processed/provenance.csv"
if os.path.exists(p):
    old = pd.read_csv(p); prov = pd.concat([old[~old.source_id.str.startswith("bea_")], prov])
prov.to_csv(p, index=False)
print(len(out), "BEA rows;", out.suppressed.sum(), "suppressed; years", out.year.min(), "-", out.year.max())
