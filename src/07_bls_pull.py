"""Pull BLS CES monthly series (SA) 2010-2026 -> data/raw/bls/ces.json, data/processed/bls.csv"""
import json, os, sys, requests, pandas as pd
from dotenv import load_dotenv
load_dotenv(); sys.path.insert(0, "src"); from redact import redact
SERIES = {"CES6054150001": "Computer systems design and related services (NAICS 5415)",
          "CES6054000001": "Professional, scientific, and technical services (NAICS 54)",
          "CES0000000001": "Total nonfarm"}
rows = []
for start, end in [("2010", "2019"), ("2020", "2026")]:
    r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", timeout=60, json={
        "seriesid": list(SERIES), "startyear": start, "endyear": end, "registrationkey": os.environ["BLS_API_KEY"]}).json()
    assert r["status"] == "REQUEST_SUCCEEDED", r.get("message")
    json.dump(redact(r), open(f"data/raw/bls/ces_{start}_{end}.json", "w"))
    for s in r["Results"]["series"]:
        for d in s["data"]:
            if d["period"].startswith("M") and d["period"] != "M13":
                rows.append(dict(series_id=s["seriesID"], series=SERIES[s["seriesID"]], date=f"{d['year']}-{d['period'][1:]}-01", value=float(d["value"]),
                                 preliminary="P" in [f.get("code") for f in d.get("footnotes", []) if f]))
df = pd.DataFrame(rows).sort_values(["series_id", "date"]); df.to_csv("data/processed/bls.csv", index=False)
print(df.groupby("series").date.agg(["min", "max", "count"]).to_string())
