"""Find and download Wipro quarterly datasheet exhibits (6-K) from EDGAR via full-text search.
Saves to data/raw/sec/wipro_datasheets/<filedate>_<accession>_<doc>."""
import os, time, requests
UA = {"User-Agent": "OffshoreAIResearch research-script admin@example.org"}
OUT = "data/raw/sec/wipro_datasheets"; os.makedirs(OUT, exist_ok=True)
r = requests.get("https://efts.sec.gov/LATEST/search-index", headers=UA, timeout=60, params={
    "q": '"Closing Employee Count"', "ciks": "0001123799", "forms": "6-K", "dateRange": "custom",
    "startdt": "2015-01-01", "enddt": "2026-11-24"}).json()
for h in sorted(r["hits"]["hits"], key=lambda h: h["_source"]["file_date"]):
    acc, doc = h["_id"].split(":"); fd = h["_source"]["file_date"]
    fn = f"{OUT}/{fd}_{acc}_{doc}"
    if os.path.exists(fn): continue
    url = f"https://www.sec.gov/Archives/edgar/data/1123799/{acc.replace('-', '')}/{doc}"
    resp = requests.get(url, headers=UA, timeout=60); resp.raise_for_status()
    open(fn, "wb").write(resp.content); time.sleep(0.15)
print(len(os.listdir(OUT)), "files")
