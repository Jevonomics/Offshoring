"""LTIMindtree now trades as LTM Limited (LTM.NS; LTIM.NS returns 404, history from the 2016 LTI listing).
Daily adjusted closes (splits and dividends) from Yahoo Finance's public chart endpoint.
Writes data/processed/stock_prices.csv (date, ticker, adjclose, currency). Missing days stay missing."""
import json, urllib.request, pandas as pd, time
TICKERS = {"TCS.NS": "TCS", "INFY.NS": "Infosys", "WIPRO.NS": "Wipro", "HCLTECH.NS": "HCLTech",
           "TECHM.NS": "TechM", "LTM.NS": "LTIMindtree", "ACN": "Accenture",
           "^NSEI": "Nifty 50", "^CNXIT": "Nifty IT", "^GSPC": "S&P 500"}
rows = []
for t, name in TICKERS.items():
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?period1=1420070400&period2={int(time.time())}&interval=1d&events=div,split"
    req = urllib.request.Request(url, headers={"User-Agent": "OffshoreAIResearch research-script"})
    r = json.load(urllib.request.urlopen(req))["chart"]["result"][0]
    adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose") or r["indicators"]["quote"][0]["close"]
    d = pd.DataFrame({"date": pd.to_datetime(r["timestamp"], unit="s") + pd.Timedelta(seconds=r["meta"]["gmtoffset"]),
                      "adjclose": adj})
    d["date"] = d.date.dt.normalize(); d["ticker"] = t; d["name"] = name; d["currency"] = r["meta"]["currency"]
    rows.append(d.dropna(subset=["adjclose"]))
    print(name, len(d), d.date.min().date(), d.date.max().date())
pd.concat(rows).to_csv("data/processed/stock_prices.csv", index=False)
