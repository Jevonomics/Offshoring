"""Download LTI / LTIMindtree / LTM 'Earnings Release and Factsheet' PDFs for FY2017-FY2027 via ltm.com's JSON index."""
import json, os, re, time, requests, pdfplumber
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
IDX = "https://www.ltm.com/content/ltimcorporatewebsite/us/investors/financial-results/jcr:content/root/container/investorfinancial.json"
OUT = "data/raw/ltim/factsheets"; os.makedirs(OUT, exist_ok=True)
for y in range(2017, 2028):
    d = requests.get(IDX, params={"year": y, "investorType": "ltimcorporatewebsite:investors/financial-results"}, headers=UA, timeout=60).json()
    json.dump(d, open(f"data/raw/ltim/index_{y}.json", "w"))
    for x in d["ltimcorporatewebsite:investors/financial-results"]:
        if "factsheet" not in x["title"].lower().replace(" ", "") and "fact sheet" not in x["title"].lower(): continue
        q = re.search(r"\d", x["investor_quarter"]).group(0); u = x["uplaod_link"]
        fn = f"{OUT}/FY{y}_Q{q}.pdf"
        if not os.path.exists(fn):
            r = requests.get(u, headers=UA, timeout=120)
            if r.ok and r.content[:4] == b"%PDF": open(fn, "wb").write(r.content)
            else: print("FAILED", y, q, r.status_code, u); continue
            time.sleep(0.3)
        with pdfplumber.open(fn) as pdf: n = sum(len(p.extract_text() or "") for p in pdf.pages)
        print(f"FY{y} Q{q}  text_chars={n:>6}  {u.rsplit('/',1)[1]}")
