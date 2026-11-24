"""Download Accenture quarterly earnings-release exhibits (8-K Item 2.02, EX-99.1) since FY2016 from EDGAR."""
import json, os, re, time, requests
UA = {"User-Agent": "OffshoreAIResearch research-script admin@example.org"}
OUT = "data/raw/sec/accenture"; os.makedirs(OUT, exist_ok=True)
sub = json.load(open("data/raw/sec/submissions_accenture.json"))
frames = [sub["filings"]["recent"]]
for f in sub["filings"].get("files", []):
    p = f"data/raw/sec/accenture_{f['name']}"
    if not os.path.exists(p):
        open(p, "w").write(requests.get(f"https://data.sec.gov/submissions/{f['name']}", headers=UA, timeout=60).text); time.sleep(.2)
    frames.append(json.load(open(p)))
got = 0
for fr in frames:
    for form, dt, acc, items in zip(fr["form"], fr["filingDate"], fr["accessionNumber"], fr["items"]):
        if form != "8-K" or "2.02" not in items or dt < "2015-09-01": continue
        base = f"https://www.sec.gov/Archives/edgar/data/1467373/{acc.replace('-', '')}"
        idx = requests.get(f"{base}/index.json", headers=UA, timeout=60).json(); time.sleep(.15)
        docs = [i["name"] for i in idx["directory"]["item"] if re.search(r"ex-?99|ex991|exhibit", i["name"], re.I) and i["name"].lower().endswith(".htm")]
        for d in docs[:1]:
            fn = f"{OUT}/{dt}_{d}"
            if not os.path.exists(fn): open(fn, "wb").write(requests.get(f"{base}/{d}", headers=UA, timeout=60).content); time.sleep(.15)
            got += 1
print(got, "earnings releases;", len(os.listdir(OUT)), "files")
