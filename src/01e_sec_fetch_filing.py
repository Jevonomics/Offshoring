"""Download every document in given EDGAR filings (htm/txt/pdf) to data/raw/sec/<firm>/<accession>/.
Usage: python -I src/01e_sec_fetch_filing.py <firm> <cik> <accession> [<accession> ...]"""
import os, re, sys, time, requests
UA = {"User-Agent": "OffshoreAIResearch research-script admin@example.org"}
firm, cik, accs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
for acc in accs:
    base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-','')}"
    out = f"data/raw/sec/{firm}/{acc}"; os.makedirs(out, exist_ok=True)
    idx = requests.get(f"{base}/index.json", headers=UA, timeout=60).json()
    for it in idx["directory"]["item"]:
        n = it["name"]
        if not re.search(r"\.(htm|html|txt|pdf|xlsx?)$", n, re.I) or n.endswith("-index.html") or n.endswith("-index-headers.html") or re.match(r"^\d{10}-\d{2}-\d{6}\.txt$", n): continue
        p = f"{out}/{n}"
        if not os.path.exists(p):
            r = requests.get(f"{base}/{n}", headers=UA, timeout=120); r.raise_for_status()
            open(p, "wb").write(r.content); time.sleep(0.15)
        print(acc, n, os.path.getsize(p))
