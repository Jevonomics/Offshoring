"""Verify BLS CES series for NAICS 5415 and fetch catalog metadata."""
import json, os, requests
from dotenv import load_dotenv
import sys; sys.path.insert(0, "src"); from redact import redact
load_dotenv()
p = {"seriesid": ["CES6054150001"], "startyear": "2024", "endyear": "2026", "catalog": True, "registrationkey": os.environ["BLS_API_KEY"]}
r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", json=p, timeout=60).json()
json.dump(redact(r), open("data/raw/bls/probe_CES6054150001.json", "w"))
print(r["status"], r.get("message"))
for s in r["Results"]["series"]:
    print(s["seriesID"], s.get("catalog", {}).get("series_title"), "|", s.get("catalog", {}).get("industry_name"))
    print("  latest:", [(d["year"], d["periodName"], d["value"]) for d in s["data"][:3]])
