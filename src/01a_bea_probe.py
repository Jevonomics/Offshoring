"""Probe BEA IntlServTrade dataset: parameter values and availability."""
import json, os, sys, requests
from dotenv import load_dotenv
import sys; sys.path.insert(0, "src"); from redact import redact
load_dotenv()
KEY = os.environ["BEA_API_KEY"]
URL = "https://apps.bea.gov/api/data"
OUT = "data/raw/bea"

def get(**p):
    p.update(UserID=KEY, ResultFormat="JSON")
    r = requests.get(URL, params=p, timeout=60); r.raise_for_status()
    return r.json()

for param in ["TypeOfService", "Affiliation", "AreaOrCountry", "TradeDirection"]:
    d = get(method="GetParameterValues", DatasetName="IntlServTrade", ParameterName=param)
    with open(f"{OUT}/params_{param}.json", "w") as f: json.dump(redact(d), f, indent=1)
    vals = d["BEAAPI"]["Results"]["ParamValue"]
    print(f"== {param}: {len(vals)} values")
    for v in vals:
        k = v.get("Key"); desc = v.get("Desc")
        if param != "AreaOrCountry" or any(s in (k or "") for s in ["India", "Philippines", "AllCountries"]):
            print("  ", k, "|", desc)
