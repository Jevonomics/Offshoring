"""Collect HCLTech quarterly investor release PDFs via the results page year filter. Saves to data/raw/hcltech/releases/."""
import os, re, time, requests
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
OUT = "data/raw/hcltech/releases"; os.makedirs(OUT, exist_ok=True)
links = set()
for y0 in range(2015, 2027):
    y = f"{y0}-{str(y0 + 1)[2:]}"
    h = requests.get("https://www.hcltech.com/investor-relations/financial-results", params={"year": y}, headers=UA, timeout=60).text
    for u in set(re.findall(r'https?://[^"\'\s<>]+\.pdf', h)):
        n = u.rsplit("/", 1)[1].lower()
        if "investor" in n and ("release" in n or n.startswith("investorrelease")): links.add((y, u))
    time.sleep(0.5)
for y, u in sorted(links):
    fn = f"{OUT}/{y}__{u.rsplit('/', 1)[1]}"
    if not os.path.exists(fn):
        r = requests.get(u, headers=UA, timeout=120)
        if r.ok and r.content[:4] == b"%PDF": open(fn, "wb").write(r.content)
        else: print("FAILED", r.status_code, u)
        time.sleep(0.3)
    print(y, os.path.basename(fn))
