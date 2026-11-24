"""Download EDGAR submission indexes for Infosys, Wipro, Cognizant, Accenture."""
import json, requests, time
UA = {"User-Agent": "OffshoreAIResearch research-script admin@example.org"}
CIKS = {"infosys": 1067491, "wipro": 1123799, "cognizant": 1058290, "accenture": 1467373}
for name, cik in CIKS.items():
    d = requests.get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", headers=UA, timeout=60).json()
    json.dump(d, open(f"data/raw/sec/submissions_{name}.json", "w"))
    r = d["filings"]["recent"]
    forms = {}
    for f, dt in zip(r["form"], r["filingDate"]): forms.setdefault(f, []).append(dt)
    print(name, d["name"], {k: (len(v), min(v), max(v)) for k, v in forms.items() if k in ("6-K","20-F","10-Q","10-K")},
          "older files:", len(d["filings"].get("files", [])))
    time.sleep(0.3)
