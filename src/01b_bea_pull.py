"""Pull BEA IntlServTrade imports for India, Philippines, AllCountries; all service types and affiliations, all years.
Writes raw JSON to data/raw/bea/ (one file per country x affiliation)."""
import json, os, requests
from dotenv import load_dotenv
import sys; sys.path.insert(0, "src"); from redact import redact
load_dotenv()
KEY = os.environ["BEA_API_KEY"]
URL = "https://apps.bea.gov/api/data"
OUT = "data/raw/bea"
for country in ["India", "Philippines", "AllCountries"]:
    for aff in ["AllAffiliations", "Affiliated", "Unaffiliated"]:
        p = dict(UserID=KEY, method="GetData", DatasetName="IntlServTrade", TypeOfService="All",
                 TradeDirection="Imports", Affiliation=aff, AreaOrCountry=country, Year="All", ResultFormat="JSON")
        r = requests.get(URL, params=p, timeout=120); r.raise_for_status()
        d = r.json()
        fn = f"{OUT}/imports_{country}_{aff}.json"
        with open(fn, "w") as f: json.dump(redact(d), f)
        res = d["BEAAPI"].get("Results", {})
        rows = res.get("Data", []) if isinstance(res, dict) else []
        err = d["BEAAPI"].get("Error") or (res.get("Error") if isinstance(res, dict) else None)
        print(country, aff, "rows:", len(rows), "err:", err)
